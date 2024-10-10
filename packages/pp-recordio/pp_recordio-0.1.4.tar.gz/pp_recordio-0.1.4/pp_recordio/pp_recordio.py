import ctypes
import platform
import os
import logging
from typing import List, Optional, Generator

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load the shared library
def load_library():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "darwin":
        if machine == "arm64":
            lib_name = "pp_recordio_lib_darwin_arm64.so"
        else:
            lib_name = "pp_recordio_lib_darwin_amd64.so"
    elif system == "linux":
        if machine == "arm64":
            lib_name = "pp_recordio_lib_linux_arm64.so"
        else:
            lib_name = "pp_recordio_lib_linux_amd64.so"
    # Windows unsupported for now.
    # elif system == "windows":
    #     lib_name = "pp_recordio_lib_windows_amd64.dll"
    else:
        raise RuntimeError(f"Unsupported system: {system}")

    lib_path = os.path.join(os.path.dirname(__file__), lib_name)
    return ctypes.CDLL(lib_path)

lib = load_library()
# lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "pp_recordio_lib.so"))

# Define C structures
class Result(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_char)),
        ("length", ctypes.c_int),
        ("error", ctypes.c_char_p)
    ]

# Define function prototypes
lib.RecordWriter.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
lib.RecordWriter.restype = ctypes.POINTER(Result)

lib.RecordReader.argtypes = [ctypes.c_char_p]
lib.RecordReader.restype = ctypes.POINTER(Result)

lib.RecordReaderNext.argtypes = [ctypes.c_char_p]
lib.RecordReaderNext.restype = ctypes.POINTER(Result)

lib.CloseRecordReader.argtypes = [ctypes.c_char_p]
lib.CloseRecordReader.restype = None

class RecordWriter:
    def __init__(self, filename: str):
        self.filename = filename.encode('utf-8')

    def write(self, data: bytes, compress: bool = False) -> None:
        result = lib.RecordWriter(data, len(data), self.filename, int(compress))
        if result.contents.error:
            raise IOError(result.contents.error.decode('utf-8'))

class RecordReader:
    def __init__(self, filename: str):
        self.filename = filename.encode('utf-8')

    def read_all(self) -> List[bytes]:
        result = lib.RecordReader(self.filename)
        if result.contents.error:
            raise IOError(result.contents.error.decode('utf-8'))
        data = ctypes.string_at(result.contents.data, result.contents.length)
        return self._deserialize_records(data)

    def read(self) -> Generator[bytes, None, None]:
        while True:
            try:
                yield self.__next__()
            except StopIteration:
                break

    def __iter__(self):
        return self

    def __next__(self) -> bytes:
        logger.debug("Calling RecordReaderNext")
        result = lib.RecordReaderNext(self.filename)
        if not result:
            logger.debug("RecordReaderNext returned NULL")
            raise StopIteration
        if result.contents.error:
            error_message = result.contents.error.decode('utf-8')
            logger.debug(f"RecordReaderNext returned error: {error_message}")
            if "EOF" in error_message:
                raise StopIteration
            logger.warning(f"Error reading record: {error_message}")
            raise IOError(error_message)
        if result.contents.length == 0:
            logger.debug("RecordReaderNext returned empty result")
            raise StopIteration
        logger.debug(f"RecordReaderNext returned {result.contents.length} bytes")
        return ctypes.string_at(result.contents.data, result.contents.length)

    def close(self) -> None:
        lib.CloseRecordReader(self.filename)

    def _deserialize_records(self, data: bytes) -> List[bytes]:
        records = []
        offset = 0
        while offset < len(data):
            record_length = int.from_bytes(data[offset:offset+4], byteorder='big')
            offset += 4
            record = data[offset:offset+record_length]
            records.append(record)
            offset += record_length
        return records

def write_records(filename: str, records: List[bytes], compress: bool = False) -> None:
    writer = RecordWriter(filename)
    for record in records:
        writer.write(record, compress)

def read_records(filename: str) -> List[bytes]:
    reader = RecordReader(filename)
    try:
        return reader.read_all()
    finally:
        reader.close()
