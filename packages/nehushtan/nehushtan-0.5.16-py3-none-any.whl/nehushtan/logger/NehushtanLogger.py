import json
import math
import os
import sys
import threading
import time
import traceback
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, List

import psutil

from nehushtan.helper.CommonHelper import CommonHelper


class NehushtanLogLevel(Enum):
    """
    Since 0.5.1.
    """
    CRITICAL = 50
    FATAL = 50
    ERROR = 40
    WARNING = 30
    WARN = 30
    NOTICE = 25
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class NehushtanLoggerAdapter(ABC):
    """
    Since 0.5.1.
    """

    def __init__(self):
        self.__topic = 'default'

    def ensure_serializable_dict(self, d: dict) -> dict:
        """
        Since 0.1.25, add ensure_ascii as False to allow Unicode chars
        """
        s = json.dumps(d, default=lambda inner_x: inner_x.__str__(), ensure_ascii=False)
        return json.loads(s)

    def transform_exception(self, e: BaseException):
        if CommonHelper.is_python_version_at_least(3, 10):
            return traceback.format_exception(e)
        else:
            return traceback.format_exception(
                etype=type(e),
                value=e,
                tb=e.__traceback__
            )

    @abstractmethod
    def write_one_log(self, level: NehushtanLogLevel, contents: dict):
        pass

    def set_topic(self, topic: str):
        self.__topic = topic

    def get_topic(self) -> str:
        return self.__topic


class NehushtanLoggerAdapterWithStdOut(NehushtanLoggerAdapter):
    """
    Since 0.5.1.
    """

    def __init__(self, record_millisecond=False, ):
        super().__init__()
        self.__record_millisecond = record_millisecond

    def _is_record_millisecond(self) -> bool:
        return self.__record_millisecond

    def prepare_log_text(self, level: NehushtanLogLevel, contents: dict):
        time_format_string = "%Y-%m-%d %H:%M:%S"
        if self.__record_millisecond:
            time_format_string += '.%f'
        now = datetime.now().strftime(time_format_string)
        level_label = f'{level.name}'
        pid = os.getpid()

        if CommonHelper.is_python_version_at_least(3, 10):
            thread = threading.current_thread()
        else:
            thread = threading.currentThread()

        clean_contents = self.ensure_serializable_dict(contents)
        message = clean_contents.get('message', '')
        del clean_contents['message']

        line = f'{now} <{self.get_topic()}> [{level_label}] <{pid}:{thread.name}> {message}'
        if len(clean_contents.keys()) > 0:
            extra_json = json.dumps(clean_contents, ensure_ascii=False)
            line += f' | {extra_json}'
        return line

    def write_one_log(self, level: NehushtanLogLevel, contents: dict):
        line = self.prepare_log_text(level, contents)
        print(line)


class NehushtanLoggerAdapterWithFileWriter(NehushtanLoggerAdapterWithStdOut):
    """
    Since 0.5.1.
    """

    def __init__(self,
                 log_dir: str,
                 categorize: bool = True,
                 date_rotate: bool = True,
                 record_millisecond=False,
                 file_encoding='utf-8',
                 ):
        super().__init__(record_millisecond=record_millisecond)

        self.__categorize = categorize

        if log_dir is None:
            raise Exception('NehushtanLoggerAdapterWithFileWriter: log_dir is None')
        self.__log_dir = log_dir

        self.__date_rotate = date_rotate

        # Since 0.4.20 CACHED FILE HANDLER
        self.__keep_file_open = True
        self.__opened_files = {}
        # Since 0.4.20 TARGET FILE ENCODING
        self.__file_encoding = file_encoding

    def set_topic(self, topic: str):
        super().set_topic(topic)
        # This logic is since 0.4.19
        if self.__categorize:
            x = topic.split('/')
            last_title = None
            y = []
            for xx in x:
                if xx:
                    if last_title:
                        y.append(last_title)
                    last_title = xx
            if y and self.__log_dir:
                self.__log_dir = self.__log_dir + '/' + ('/'.join(y))
            if last_title:
                super().set_topic(last_title)

    def __del__(self):
        if len(self.__opened_files.items()) > 0:
            for name, file in self.__opened_files.items():
                file.close()
                # print(name, 'closed')

    def __get_target_file(self):
        if self.__log_dir is None:
            raise Exception('NehushtanLoggerAdapterWithFileWriter: log_dir is None')

        category_dir = self.__log_dir

        # a -> a/a-DATE.log
        # a/b -> a/b-DATE.log
        # a/b/c -> a/b/c-DATE.log

        if self.__categorize:
            category_dir = os.path.join(self.__log_dir, self.get_topic())

        today = ''
        if self.__date_rotate:
            today = time.strftime("%Y%m%d", time.localtime())
            today = f'-{today}'

        target_file = os.path.join(category_dir, f'{self.get_topic()}{today}.log')

        final_dir = os.path.dirname(target_file)
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        return target_file

    def __get_target_file_handler(self, target_file_path: str):
        if not target_file_path:
            raise Exception('NehushtanLoggerAdapterWithFileWriter: target_file_path is None')

        if self.__keep_file_open:
            file = self.__opened_files.get(target_file_path)
            if not file:
                file = open(target_file_path, 'a', encoding=self.__file_encoding)
                self.__opened_files[target_file_path] = file
        else:
            file = open(target_file_path, 'a', encoding=self.__file_encoding)

        return file

    def write_raw_line_to_log(self, text: str, end=os.linesep):
        target_file = self.__get_target_file()

        if target_file != '':
            file = self.__get_target_file_handler(target_file)
            file.write(text + end)
            file.flush()

            if not self.__keep_file_open:
                file.close()

        return self

    def write_one_log(self, level: NehushtanLogLevel, contents: dict):
        """
        Since 0.3.7 add `hide_extra`
        """
        line = self.prepare_log_text(level, contents)
        return self.write_raw_line_to_log(line)


class NehushtanLogger:
    """
    Since 0.5.1.
    """

    def __init__(self,
                 topic: str = 'default',
                 adapter: NehushtanLoggerAdapter = NehushtanLoggerAdapterWithStdOut(),
                 log_level: NehushtanLogLevel = NehushtanLogLevel.DEBUG,
                 print_higher_than_this_level: NehushtanLogLevel = NehushtanLogLevel.CRITICAL,
                 default_context: Optional[dict] = None,
                 ):
        self.__topic = topic
        self.__adapter = adapter
        self.__adapter.set_topic(topic)
        self.__log_level = log_level
        self.__default_context = default_context

        # self.print_as_well = print_as_well <-- should use print_higher_than_this_level=NehushtanLogging.NOTSET
        # If all, use NOTSET; if none, use FATAL
        self.__print_higher_than_this_level = print_higher_than_this_level
        if self.__print_higher_than_this_level.value < NehushtanLogLevel.FATAL.value:
            self.__adapter_with_stdout = NehushtanLoggerAdapterWithStdOut()

    def get_adapter(self) -> NehushtanLoggerAdapter:
        return self.__adapter

    def get_traceback_info_from_exception(self, e: BaseException) -> List[str]:
        return self.__adapter.transform_exception(e)

    def write_one_log(self, level: NehushtanLogLevel, contents: dict):
        if self.__default_context is not None:
            context = contents.get('context')
            if context is None:
                contents['context'] = self.__default_context
            else:
                if isinstance(context, dict):
                    c = {}
                    c.update(self.__default_context)
                    c.update(context)
                    contents['context'] = c
                else:
                    pass
        self.get_adapter().write_one_log(level, contents)
        if level.value > self.__print_higher_than_this_level.value:
            self.__adapter_with_stdout.write_one_log(level, contents)

    def _log(self, level: NehushtanLogLevel, message: str, context: Optional[dict] = None):
        if level.value >= self.__log_level.value:
            contents = {'message': message}
            if context is not None:
                contents['context'] = context
            self.write_one_log(level=level, contents=contents)

    def debug(self, message: str, extra: Optional[dict] = None):
        self._log(level=NehushtanLogLevel.DEBUG, message=message, context=extra)

    def info(self, message: str, extra: Optional[dict] = None):
        self._log(level=NehushtanLogLevel.INFO, message=message, context=extra)

    def notice(self, message: str, extra: Optional[dict] = None):
        self._log(level=NehushtanLogLevel.NOTICE, message=message, context=extra)

    def warning(self, message: str, extra: Optional[dict] = None):
        self._log(level=NehushtanLogLevel.WARNING, message=message, context=extra)

    def error(self, message: str, extra: Optional[dict] = None):
        self._log(level=NehushtanLogLevel.ERROR, message=message, context=extra)

    def critical(self, message: str, extra: Optional[dict] = None):
        self._log(level=NehushtanLogLevel.CRITICAL, message=message, context=extra)

    def exception(self, message: str, e: BaseException):
        level = NehushtanLogLevel.ERROR
        traces = self.get_adapter().transform_exception(e)
        if level.value >= self.__log_level.value:
            contents = {
                'message': message,
                'exception': {
                    'class': e.__class__.__name__,
                    'message': e.__str__(),
                    'trace': traces,
                }
            }
            self.write_one_log(level=level, contents=contents)

    def log_progress(
            self,
            title: str,
            done_task_count: int,
            total_task_count: int = 100,
            progress_bar_length: int = 20,
            desc: str = None,
            level: NehushtanLogLevel = NehushtanLogLevel.NOTICE
    ):
        percent = 100.0 * done_task_count / total_task_count
        bar = ''
        done_bar_chars = math.floor(progress_bar_length * percent / 100.0)
        for i in range(done_bar_chars):
            bar += '='
        for j in range(progress_bar_length - done_bar_chars):
            bar += '-'

        content = f'{title}: {percent:2.2f}% ({done_task_count}/{total_task_count}) [{bar}]'
        if desc is not None:
            content += f' {desc}'

        self._log(level=level, message=content, )

    def log_current_memory_usage_of_process(self, pid: int = None, level: NehushtanLogLevel = NehushtanLogLevel.INFO):
        """
        Filed `pid` would use os.getpid() for None.
        """
        memory_usage = psutil.Process(pid=pid).memory_info()
        self._log(
            level,
            'Current Memory Usage Snapshot (in MB)',
            {'rss': memory_usage.rss / 1024.0 / 1024.0, 'vms': memory_usage.vms / 1024.0 / 1024.0}
        )

    def log_current_memory_usage_of_object(self, target_name: str, target,
                                           level: NehushtanLogLevel = NehushtanLogLevel.INFO):

        memory_usage = sys.getsizeof(target)
        self._log(
            level,
            f'Current Memory Usage used by {target_name} (in MB)',
            {'size': memory_usage / 1024.0 / 1024.0}
        )
