import asyncio
from classes.FileProtocol import EchoClientProtocol

loop = asyncio.get_event_loop()
message = 'Hello World!'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()