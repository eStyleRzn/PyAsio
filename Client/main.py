import asyncio
from classes.ClientTransceiver import ClientTransceiver

loop = asyncio.get_event_loop()
message = 'Hello World!'
data_exchange = loop.create_connection(lambda: ClientTransceiver(message, loop), '127.0.0.1', 8888)
loop.run_until_complete(data_exchange)
loop.run_forever()
loop.close()