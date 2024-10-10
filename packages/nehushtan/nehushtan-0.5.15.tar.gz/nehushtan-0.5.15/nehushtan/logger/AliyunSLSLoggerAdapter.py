import json
import time
from typing import List

from aliyun.log import LogClient, PutLogsRequest, LogItem, LogException

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.logger.NehushtanLogger import NehushtanLoggerAdapter, NehushtanLogLevel


class AliyunSLSLoggerAdapter(NehushtanLoggerAdapter):
    """
    Adapter for Aliyun SLS.
    Requirement `aliyun-log-python-sdk` (such as 0.9.11) should be declared.
    Since 0.5.1.
    """

    def __init__(self,
                 endpoint: str,
                 access_key_id: str,
                 access_key_secret: str,
                 project: str,
                 logstore: str,
                 source: str,
                 with_buffer: bool = False,
                 buffer_size: int = 100,
                 ):
        super().__init__()
        self.__client = LogClient(endpoint, access_key_id, access_key_secret)
        self.__logstore = logstore
        self.__project = project
        self.__source = source.replace('[IP]', CommonHelper.get_local_ip())
        self.__with_buffer = with_buffer
        self.__buffer = []
        self.__buffer_size = buffer_size

    def write_one_log(self, level: NehushtanLogLevel, contents: dict):
        if self.__with_buffer:
            return self.__write_one_log_into_buffer(level, contents)
        else:
            return self.__write_one_log_directly(level, contents)

    def __write_one_log_directly(self, level: NehushtanLogLevel, contents: dict):
        # topic = contents['topic']
        # del contents['topic']
        contents['level'] = level.name

        l = []
        for (k, v) in contents.items():
            if v is None:
                l.append((k, None,))
            elif isinstance(v, str):
                l.append((k, v))
            else:
                l.append((k, json.dumps(v, default=lambda x: x.__str__(), ensure_ascii=False)))

        log_item = LogItem()
        log_item.set_time(int(time.time()))
        log_item.set_contents(l)

        self.__send_to_sls([log_item])

    def __write_one_log_into_buffer(self, level: NehushtanLogLevel, contents: dict):
        contents['level'] = level.name
        self.__buffer.append(contents)

        if len(self.__buffer) >= self.__buffer_size:
            self.flush_buffer()

    def flush_buffer(self):
        if len(self.__buffer) == 0:
            return

        buffer = self.__buffer
        self.__buffer = []

        log_item_list = []
        for contents in buffer:
            l = []
            for (k, v) in contents.items():
                if v is None:
                    l.append((k, None,))
                elif isinstance(v, str):
                    l.append((k, v))
                else:
                    l.append((k, json.dumps(v, default=lambda x: x.__str__(), ensure_ascii=False)))

            log_item = LogItem()
            log_item.set_time(int(time.time()))
            log_item.set_contents(l)

            log_item_list.append(log_item)

        self.__send_to_sls(log_item_list)

    def __send_to_sls(self, log_item_list: List[LogItem]):
        req2 = PutLogsRequest(
            project=self.__project,
            logstore=self.__logstore,
            topic=self.get_topic(),
            source=self.__source,
            logitems=log_item_list,
        )
        try:
            self.__client.put_logs(req2)
        except LogException as e:
            print(e)

    def __del__(self):
        if self.__with_buffer and len(self.__buffer) > 0:
            self.flush_buffer()
