import asyncio
import zlib
import hashlib
import random
import sys

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
        # Close the file for sure
        if self._file_obj:
            self._file_obj.close()

        print('Transceiver id=' + str(id(self)) + ' is destroyed')

    def _write(self, str_data):
        out_bytes = zlib.compress(str_data.encode(), 1)
        self._transport.write(out_bytes)

    def _read(self, data):
        in_bytes = zlib.decompress(data)
        return in_bytes.decode()

    def _calc_hash(self):
        # Calculate hash of the file. For this task we do not face any security issues, so use md5 algorithm
        hash_md5 = hashlib.md5()
        with open(self._file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _gen_upload_id(self):
        return str(random.randrange(sys.maxsize))

