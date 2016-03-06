import base64
import asyncio
import json
import os
from pathlib import Path

# ======================================================================================================================
class ClientTransceiver(asyncio.Protocol):
    chunk_size_bytes = 1024 * 1
    def __init__(self, file_path, loop):

        # TODO throw an exception if the file_path is invalid
        self.file_path = file_path
        self.loop = loop
        self.current_chunk = 0
        self.transport = None
        self.file_obj = None
        self.__is_new_file = None
        self.__file_size = None
        self.__file_name = None
        self.__upload_id = None

    def __del__(self):
        if self.file_obj:
            self.file_obj.close()

    def connection_made(self, transport):
        # Evaluate the transport instance
        self.transport = transport

        # Initialize upload session data
        self.__is_new_file = True
        self.__file_name = Path(self.file_path).name
        self.__file_size = os.path.getsize(self.file_path)

        # Open the file for reading
        self.file_obj = open(self.file_path, 'rb')

        if not self.send_data():
            self.loop.stop()

    def data_received(self, data):
        # Parse input to the Python objects
        input = json.loads(data.decode())

        # Validate upload id
        if not self.__upload_id:
            self.__upload_id = input['upload_id']
        else:
            # Validate it!
            self.__upload_id = self.__upload_id

        file_rest = input['rest']

        if 0 >= file_rest:
            self.loop.stop()

        # TODO Validate hash

        if not self.send_data():
            self.loop.stop()

        print('Data received. File rest: {!r}'.format(input['rest']))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

    def send_data(self):
        # Read anew data chunk from the file
        data = self.file_obj.read(ClientTransceiver.chunk_size_bytes)

        if not len(data):
            return False

        # Wrap file content into json packet
        outs = self.__json_data(data).encode()

        # Transmit the packet
        self.transport.write(outs)

        print('Data sent!')
        return True

    def __json_data(self, data):

        # encode read data to the Base64
        enc_data = base64.b64encode(data).decode()

        if self.__is_new_file:
            self.__is_new_file = False

            # Create header packet
            outs = json.dumps({'mime_type': 'application/octet-stream', \
                               'size': self.__file_size, \
                               'name': self.__file_name, \
                               'data': enc_data})
        else:
            # Create chunk packet
            outs = json.dumps({'mime_type': 'application/octet-stream', \
                               'upload_id': self.__upload_id, \
                               'data': enc_data})

        dummy = json.loads(outs)
        return outs
