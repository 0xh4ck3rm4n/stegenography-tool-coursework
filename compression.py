# imported libraries
import zlib
import lzma

ZLIB_COMPRESSION_LEVEL = 9  # Maximum compression

def compress_data(data: bytes, method: str = 'zlib') -> bytes:
    if method == 'lzma':
        return lzma.compress(data, preset=9)
    else: 
        return zlib.compress(data, ZLIB_COMPRESSION_LEVEL)

def decompress_data(data: bytes, method: str = 'zlib') -> bytes:

    try:
        if method == 'lzma':
            return lzma.decompress(data)
        else:  # zlib default
            return zlib.decompress(data)
    except Exception:
        return None

def get_compression_ratio(original_size: int, compressed_size: int) -> float:

    if original_size == 0:
        return 0.0
    return round((1 - compressed_size / original_size) * 100, 1)
