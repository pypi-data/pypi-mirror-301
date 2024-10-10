import time
from datetime import datetime

from aliyun.log import LogClient, LogItem, PutLogsRequest

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.logger.AliyunSLSLoggerAdapter import AliyunSLSLoggerAdapter
from nehushtan.logger.NehushtanLogger import NehushtanLogger
from tests.config import ALIYUN_SLS_CONFIG

endpoint = ALIYUN_SLS_CONFIG.get('endpoint')  # 选择与上面步骤创建Project所属区域匹配的Endpoint
accessKeyId = ALIYUN_SLS_CONFIG.get('accessKeyId')  # 使用你的阿里云访问密钥AccessKeyId
accessKey = ALIYUN_SLS_CONFIG.get('accessKeySecret')  # 使用你的阿里云访问密钥AccessKeySecret
project = ALIYUN_SLS_CONFIG.get('project')  # 上面步骤创建的项目名称
logstore = ALIYUN_SLS_CONFIG.get('logstore')  # 上面步骤创建的日志库名称

topic = "NehushtanTest"
source: str = ALIYUN_SLS_CONFIG.get('source')


# source = source.replace('[IP]', CommonHelper.get_local_ip())


def test_raw():
    # 构建一个client
    client = LogClient(endpoint, accessKeyId, accessKey)
    print(f'client: {client}')

    logItem = LogItem()
    logItem.set_time(int(time.time()))
    logItem.set_contents([
        ("message", CommonHelper.generate_random_uuid_hex()),
    ])

    req2 = PutLogsRequest(
        project=project,
        logstore=logstore,
        topic=topic,
        source=source.replace('[IP]', CommonHelper.get_local_ip()),
        logitems=[logItem]
    )
    res2 = client.put_logs(req2)
    res2.log_print()


def test_class():
    logger = NehushtanLogger(
        topic=topic,
        adapter=AliyunSLSLoggerAdapter(
            endpoint=endpoint,
            access_key_id=accessKeyId,
            access_key_secret=accessKey,
            project=project,
            logstore=logstore,
            source=source,
        )
    )

    logger.info('long live sinri', {'now': datetime.now()})

    try:
        d = {}
        p = d['p']
    except Exception as e:
        logger.exception('miao!', e)


if __name__ == '__main__':
    test_class()