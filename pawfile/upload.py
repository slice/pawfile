__all__ = ['handle_upload']

import hashlib
import io
import os

from flask import current_app as app


def handle_upload(file) -> str:
    """Handle the uploading of a file."""
    file_directory = app.config['UPLOADED_FILES']

    with io.BytesIO() as buffer:
        file.save(buffer)
        buffer.seek(0)
        content = buffer.read()

    # Calculate the hash of the buffer using SHA256.
    digest = hashlib.sha256(content).hexdigest()

    path = os.path.join(file_directory, digest)

    # The file is not already on the filesystem, write it.
    if not os.path.isfile(path):
        app.logger.info('Writing file. size=%d', len(content))

        with open(path, 'wb') as file:
            file.write(content)

    return digest
