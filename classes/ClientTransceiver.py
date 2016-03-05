import asyncio

# ======================================================================================================================
class ClientTransceiver(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.chunks = 20
        self.current_chunk = 0
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        if not self.send_data():
            self.loop.stop()

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

        if not self.send_data():
            self.loop.stop()

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

    def send_data(self):
        if self.current_chunk < self.chunks:
            self.transport.write(self.message.encode())
            self.current_chunk += 1

            print('Data sent: {!r}'.format(self.message))
            return True
        else:
            return False
