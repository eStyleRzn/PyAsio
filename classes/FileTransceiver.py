import asyncio
import zlib

# ======================================================================================================================
class  FileTransceiver(asyncio.Protocol):
    def __init__(self):

        super(FileTransceiver, self).__init__()

        self._transport = None
        self._file_path = None
        self._file_obj = None
        self._file_size = None
        self._upload_id = None

    def __del__(self):
        if self._file_obj:
            self._file_obj.close()

        print('Transceiver id=' + str(id(self)) + ' is destroyed')

    def _write(self, str_data):
        out_bytes = zlib.compress(str_data.encode(), 1)
        self._transport.write(out_bytes)

    def _read(self, data):
        in_bytes = zlib.decompress(data)
        return in_bytes.decode()
