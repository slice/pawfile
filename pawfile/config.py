"""Default configuration."""

import os

UPLOADED_FILES = os.path.abspath(os.path.join(
    os.path.realpath(__file__),
    '..',
    '..',
    'files',
))

# Should be changed in user configurations.
PASSWORD = os.urandom(256)
