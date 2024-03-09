from typing import Union
import zlib
import sys


def inflate(data: Union[bytes, bytearray]) -> bytes:
    """
    Decompresses zlib-compressed data.

    Usage: cat <path> | python3 inflate.py
    """
    return zlib.decompress(data)


if __name__ == "__main__":
    data = inflate(sys.stdin.buffer.read())
    sys.stdout.buffer.write(data)
