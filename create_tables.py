import traceback

from pawfile.models import File
from pawfile.db import db

try:
    with db:
        db.create_tables([File])
except Exception:
    traceback.print_exc()
    print('\N{BALLOT X} Failed to create tables.')
else:
    print('\N{CHECK MARK} Created tables.')
