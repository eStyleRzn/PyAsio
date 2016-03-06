import asyncio
from pathlib import Path
from classes.ClientTransceiver import ClientTransceiver

file_path = 'c:/Temp/Oleg/Python/python-3.5.1-amd64.exe'
path_obj = Path(file_path)

if path_obj.exists():
    loop = asyncio.get_event_loop()
    data_exchange = loop.create_connection(lambda: ClientTransceiver(file_path, loop), '127.0.0.1', 8888)
    loop.run_until_complete(data_exchange)
    loop.run_forever()
    loop.close()