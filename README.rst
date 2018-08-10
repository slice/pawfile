pawfile
=======

A small file server written in Python 3.7 and Flask.

Features
--------

* File creation
* File deletion
* Basic password authentication via ``Authorization`` header

Missing Features
~~~~~~~~~~~~~~~~

* Caching (!!!)
* File editing
* Multiple users

Setting up
----------

Clone the repository somewhere, and run ``create_tables.py``::

    python3 create_tables.py files.db

Create your configuration file, ``config.py``::

    PASSWORD = 'used to upload and delete stuff'

Install dependencies with `poetry`::

    poetry install

Start the application::

    CONFIG=config.py some_wsgi_server pawfile.app

For Development
~~~~~~~~~~~~~~~

Run the steps above and start Flask's development server::

    CONFIG=config.py FLASK_APP=pawfile.app FLASK_ENV=development flask run

Advanced Configuration
----------------------

Look at ``pawfile/config.py`` for the default configuration. You can override
those values in your own configuration file.
