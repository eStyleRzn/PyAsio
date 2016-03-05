import asyncio

# ======================================================================================================================
class  ServerTransceiver(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(id(transport))
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        response = 'Response from the transceiver object id=' + str(id(self.transport))
        print('Send: {!r}'.format(response))
        self.transport.write(str.encode(response))

        # print('Close the client socket')
        # self.transport.close()

    def connection_lost(self, exc):
        print('Client connection is lost. Transceiver id=' + str(id(self)) + ' is destroyed')
        return super(ServerTransceiver, self).connection_lost(exc)
