import shutil

from nehushtan.logger.NehushtanLogger import NehushtanLogger, NehushtanLoggerAdapterWithFileWriter
from tests.queue.plan2.Test2NehushtanQueue import Test2NehushtanQueue
from tests.queue.plan2.Test2NehushtanQueueDelegate import Test2NehushtanQueueDelegate
from tests.queue.plan2.Test2NehushtanQueueTaskDelegate import Test2NehushtanQueueTaskDelegate

if __name__ == '__main__':
    shutil.rmtree('path/to/nehushtan/log/queue-plan2')

    config_dictionary = {}
    logger = NehushtanLogger(topic='loop',
                             adapter=NehushtanLoggerAdapterWithFileWriter(
                                 log_dir='path/to/nehushtan/log/queue-plan2'))
    delegate = Test2NehushtanQueueDelegate(config_dictionary, logger)
    task_delegate = Test2NehushtanQueueTaskDelegate(config_dictionary, logger)

    Test2NehushtanQueue(delegate, task_delegate).loop()
