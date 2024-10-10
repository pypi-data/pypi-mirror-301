import asyncio

import websockets

from nehushtan.logger.NehushtanLogger import NehushtanLogger, NehushtanLoggerAdapterWithFileWriter
from tests.ws.TestWebsocketAgent import TestWebsocketAgent
from tests.ws.TestWebsocketRegisterAgent import TestWebsocketRegisterAgent


def daemon():
    request_handle_logger = NehushtanLogger(topic='ws-request',
                                            adapter=NehushtanLoggerAdapterWithFileWriter(
                                                log_dir='/Users/leqee/code/nehushtan/log/ws'))
    broadcast_logger = NehushtanLogger(topic='ws-broadcast', adapter=NehushtanLoggerAdapterWithFileWriter(
        log_dir='/Users/leqee/code/nehushtan/log/ws'))

    TestWebsocketAgent.register_agent = TestWebsocketRegisterAgent()
    agent = TestWebsocketAgent(
        broadcast_sleep_seconds=5,
        request_handle_logger=request_handle_logger,
        broadcast_logger=broadcast_logger
    )
    start_server = websockets.serve(agent.ws_request_handler, "localhost", 8080)
    asyncio.get_event_loop().create_task(agent.ws_broadcast_handler())
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    daemon()
