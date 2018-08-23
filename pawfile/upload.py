__all__ = ['read_buffer', 'hash_buffer', 'hash_exists', 'write_file']

import hashlib
import io
import os
import typing

from flask import current_app as app


def read_buffer(file) -> typing.BinaryIO:
    """Return a Werkzeug file attachment as a BinaryIO."""
    with io.BytesIO() as buffer:
        file.save(buffer)
        buffer.seek(0)
        return buffer.read()


def hash_buffer(buffer: typing.BinaryIO) -> str:
    """Return the SHA256 hash of a buffer."""
    return hashlib.sha256(buffer).hexdigest()


def hash_exists(hash: str) -> bool:
    """Check if a hash exists in the files directory."""
    file_directory = app.config['UPLOADED_FILES']
    path = os.path.join(file_directory, hash)
    return os.path.isfile(path)


def write_file(hash: str, buffer: typing.BinaryIO):
    """Write a file to the files directory using its hash as a filename."""
    file_directory = app.config['UPLOADED_FILES']
    path = os.path.join(file_directory, hash)

    app.logger.info('Writing file. size=%d', len(buffer))

    with open(path, 'wb') as file:
        file.write(buffer)
