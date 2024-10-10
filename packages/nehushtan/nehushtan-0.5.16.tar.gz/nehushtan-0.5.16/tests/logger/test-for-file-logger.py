import logging
from datetime import datetime

from nehushtan.logger.legacy.NehushtanFileLogger import NehushtanFileLogger
from nehushtan.logger.legacy.NehushtanLogging import NehushtanLogging
from nehushtan.logger.NehushtanLogger import NehushtanLogger, NehushtanLoggerAdapterWithStdOut, \
    NehushtanLoggerAdapterWithFileWriter
from tests.config import LOGGER_CONFIG

log_dir = LOGGER_CONFIG['log_dir']


def test_nehushtan_file_logger():
    file_logger = NehushtanFileLogger('test', log_dir, log_level=logging.INFO,
                                      print_higher_than_this_level=NehushtanLogging.INFO,
                                      record_millisecond=True)

    file_logger.critical('C', {"A": "B"})
    file_logger.error('E', 111)
    file_logger.warning('W', 'dd')
    file_logger.info('I', file_logger)
    file_logger.debug('D')

    try:
        raise ValueError('A<>B')
    except Exception as error:
        file_logger.exception('X', error)

    args_json = file_logger.get_args_json_to_clone()
    print(args_json)
    cloned_logger = NehushtanFileLogger.build_instance_from_args_json(args_json)

    cloned_logger.critical('C', {"A": "B"})
    cloned_logger.error('E', 111)
    cloned_logger.warning('W', 'dd')
    cloned_logger.info('I', cloned_logger)
    cloned_logger.debug('D')

    try:
        raise ValueError('A<>B')
    except Exception as error:
        cloned_logger.exception('X', error)

    progress_logger = NehushtanFileLogger()
    total = 36
    for i in range(total):
        progress_logger.log_progress('TEST', i, total, desc=f'now done[{i}]')


def test_nehushtan_logger_with_stdout_adapter():
    logger = NehushtanLogger(
        topic='default',
        adapter=NehushtanLoggerAdapterWithStdOut(),
    )
    logger.info('kakaka', {"d": "g"})


def test_nehushtan_logger_with_file_writer_adapter():
    logger = NehushtanLogger(
        topic='test/file/log',
        adapter=NehushtanLoggerAdapterWithFileWriter(
            log_dir=log_dir,
            record_millisecond=True
        )
    )
    logger.info('kakaka', {"d": "g"})

    try:
        d = {"k": datetime(year=2024, month=1, day=1), }
        logger.notice('date', d)
        p = d['p']
    except Exception as error:
        logger.exception('error', error)


if __name__ == '__main__':
    test_nehushtan_logger_with_stdout_adapter()
    test_nehushtan_logger_with_file_writer_adapter()
