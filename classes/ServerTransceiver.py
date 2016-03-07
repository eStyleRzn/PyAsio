import base64
import json
from pathlib import Path
from classes.FileTransceiver import FileTransceiver

# ======================================================================================================================
class  ServerTransceiver(FileTransceiver):
    def __init__(self):

        super(ServerTransceiver, self).__init__()

        self.__out_dir = Path().cwd()
        self.__file_rest = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(id(transport))
        print('Connection from {}'.format(peername))
        self._transport = transport

    def data_received(self, data):
        # submit input
        self.__process_received(data)

        # send response
        self.__response()

    def connection_lost(self, exc):
        self._file_obj.close()

        print('Client connection is lost.')
        return super(ServerTransceiver, self).connection_lost(exc)

    def __process_received(self, data):

        # Parse input to the Python objects
        input = json.loads(self._read(data))

        # New file or a chunk
        if 'name' in input.keys():
            self._file_size = input['size']
            self._file_rest = self._file_size

            # TODO Generate new upload_id
            self._upload_id = 'v0k84B0AT9fYkfMUp0sBTA'

            # Open destination file to write data
            file_path = str(self.__out_dir) + '/' + input['name']
            self._file_obj = open(file_path, 'wb')

            print('Receiving file: ' + file_path)
        else:
            upload_id = input['upload_id']
            # TODO validate upload_id
            if self._upload_id != upload_id:
                print('Error. upload_id mismatch!')

        # Get data
        data = input['data']

        # decode data from base64
        decoded = base64.b64decode(data)

        # Write data to the file
        self._file_obj.write(decoded)

        # Calc rest of the file
        self._file_rest -= len(decoded)

    def __response(self):

        # Make json packet
        upload_id = self._upload_id
        rest = self._file_rest
        hash_str = ''

        if 0 >= self._file_rest:
            # TODO Calculate file's hash
            self._file_obj.close()
            hash_str = 'fsgdsd234fdf'

        # Send response back to the client
        outs = json.dumps({'upload_id': upload_id, 'rest': rest, 'hash': hash_str})
        self._write(outs)

        response = 'Response from the transceiver object id=' + str(id(self._transport))
        print('Send: {!r}'.format(response))