import base64
import json
import os
from pathlib import Path
from classes.FileTransceiver import FileTransceiver

# ======================================================================================================================
class ClientTransceiver(FileTransceiver):
    chunk_size_bytes = 1024 * 1
    def __init__(self, file_path, loop, progress_callback):

        super(ClientTransceiver, self).__init__()

        # TODO throw an exception if the file_path is invalid
        self._file_path = file_path

        self.__loop = loop
        self.__current_chunk = 0
        self.__is_new_file = None
        self.__file_name = None
        self.__progress_callbck = progress_callback

    def connection_made(self, transport):
        # Evaluate the transport instance
        self._transport = transport

        # Initialize upload session data
        self.__is_new_file = True
        self.__file_name = Path(self._file_path).name
        self._file_size = os.path.getsize(self._file_path)

        # Open the file for reading
        self._file_obj = open(self._file_path, 'rb')

        if not self.__send_data():
            self.__loop.stop()

    def data_received(self, data):
        # Parse input to the Python objects
        input = json.loads(self._read(data))

        # Validate upload id
        if not self._upload_id:
            self._upload_id = input['upload_id']
        else:
            # TODO Validate it!
            self._upload_id = self._upload_id

        file_rest = input['rest']

        if 0 >= file_rest:
            # TODO Validate hash

            self._file_obj.close()
            self.__loop.stop()
        else:
            if not self.__send_data():
                self._file_obj.close()
                self.__loop.stop()

        print('Data received. File rest: {!r}'.format(input['rest']))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.__loop.stop()

    def __send_data(self):
        # Read anew data chunk from the file
        data = self._file_obj.read(ClientTransceiver.chunk_size_bytes)

        if not len(data):
            return False

        # Wrap file content into json packet and transmit it
        self._write(self.__json_data(data))

        # Call the callback to increment the progress
        self.__progress_callbck(len(data))

        return True

    def __json_data(self, data):

        # encode read data to the Base64
        enc_data = base64.b64encode(data).decode()

        if self.__is_new_file:
            self.__is_new_file = False

            # Create header packet
            outs = json.dumps({'mime_type': 'application/octet-stream', \
                               'size': self._file_size, \
                               'name': self.__file_name, \
                               'data': enc_data})
        else:
            # Create chunk packet
            outs = json.dumps({'mime_type': 'application/octet-stream', \
                               'upload_id': self._upload_id, \
                               'data': enc_data})

        dummy = json.loads(outs)
        return outs
