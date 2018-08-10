import sys
import traceback

from pawfile.models import File
from pawfile.db import db

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: create_tables.py <database file>')
        sys.exit(-1)

    db.init(sys.argv[1])

    try:
        with db:
            db.create_tables([File])
    except Exception:
        traceback.print_exc()
        print('\N{BALLOT X} Failed to create tables.')
    else:
        print('\N{CHECK MARK} Created tables.')
