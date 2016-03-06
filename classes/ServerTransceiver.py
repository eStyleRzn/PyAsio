import asyncio
import base64
import json
from pathlib import Path

# ======================================================================================================================
class  ServerTransceiver(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.file_path = None
        self.file_obj = None
        self.out_dir = Path().cwd()
        self.__file_size = None
        self.__file_rest = None
        self.__upload_id = None

    def __del__(self):
        if self.file_obj:
            self.file_obj.close()

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(id(transport))
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        # submit input
        self.__process_received(data)

        # send response
        self.__response()

    def connection_lost(self, exc):
        self.file_obj.close()
        print('Client connection is lost. Transceiver id=' + str(id(self)) + ' is destroyed')
        return super(ServerTransceiver, self).connection_lost(exc)

    def __process_received(self, data):

        # Parse input to the Python objects
        dummy = data.decode()
        input = json.loads(dummy)
        # input = json.load(data)

        # New file or a chunk
        if 'name' in input.keys():
            self.__file_size = input['size']
            self.__file_rest = self.__file_size

            # TODO Generate new upload_id
            self.__upload_id = 'v0k84B0AT9fYkfMUp0sBTA'

            # Open destination file to write data
            file_path = str(self.out_dir) + '/' + input['name']
            self.file_obj = open(file_path, 'wb')

            print('Receiving file: ' + file_path)
        else:
            upload_id = input['upload_id']
            # TODO validate upload_id
            if self.__upload_id != upload_id:
                print('Error. upload_id mismatch!')

        # Get data
        data = input['data']

        # decode data from base64
        decoded = base64.b64decode(data)

        # Write data to the file
        self.file_obj.write(decoded)

        # Calc rest of the file
        self.__file_rest -= len(decoded)

    def __response(self):

        # Make json packet
        upload_id = self.__upload_id
        rest = self.__file_rest
        hash_str = ''

        if 0 >= self.__file_rest:
            # TODO Calculate file's hash
            hash_str = 'fsgdsd234fdf'

        # Send response back to the client
        outs = json.dumps({'upload_id': upload_id, 'rest': rest, 'hash': hash_str})
        self.transport.write(outs.encode())

        response = 'Response from the transceiver object id=' + str(id(self.transport))
        print('Send: {!r}'.format(response))