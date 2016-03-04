import asyncio
from classes.FileProtocol import EchoServerClientProtocol

loop = asyncio.get_event_loop()

# Each client connection will create a new protocol instance
serverObj = loop.create_server(EchoServerClientProtocol, None, 8888)
server = loop.run_until_complete(serverObj)

# Serve requests until Ctrl+C is pressed
print('Listening for incoming connections on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
