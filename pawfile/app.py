import os
import mimetypes
import urllib.parse

from flask import Flask, request, jsonify, send_file, make_response

from . import __version__ as version
from .decorators import password_required
from .db import db
from .models import File
from .name import generate_name
from .upload import read_buffer, hash_buffer, hash_exists, write_file

app = Flask(__name__)
app.config.from_object('pawfile.config')

# Load a configuration from the CONFIG environment variable.  It is a filename
# of a .py file which is loaded.
if 'CONFIG' in os.environ:
    app.config.from_envvar('CONFIG')

db.init(app.config['DATABASE_PATH'])


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route('/')
def index():
    return jsonify(dict(version=version))


@app.route('/<file_id>', methods=['GET'])
def view(file_id):
    try:
        file = File.get(File.id == file_id)

        path = os.path.join(
            app.config['UPLOADED_FILES'],
            file.hash,
        )

        # Properly escape the filename for the Content-Disposition header.
        filename = urllib.parse.quote_plus(file.name)

        resp = make_response(send_file(
            filename_or_fp=path,
            mimetype=file.mime,
        ))

        resp.headers['Content-Disposition'] = (
            # Yes, this is quite odd. Blame backwards compatibility.
            f"inline; filename*=UTF-8''{filename}"
        )

        return resp
    except File.DoesNotExist:
        return '', 404


@app.route('/<selector>', methods=['DELETE'])
@password_required
def delete(selector):
    try:
        file = File.get(
            (File.hash == selector) | (File.id == selector)
        )
        file.delete_instance()
        return '', 204
    except File.DoesNotExist:
        return jsonify(dict(error='file not found')), 404


@app.route('/', methods=['POST'])
@password_required
def upload():
    if 'file' not in request.files:
        return jsonify(error='no file provided'), 400

    file = request.files['file']
    filename = file.filename

    # Determine the file's MIME from its filename, falling back to the one
    # provided by the uploader.
    guessed_mime = mimetypes.guess_type(filename, strict=False)[0]
    mime = guessed_mime or file.content_type

    app.logger.info(
        'Creating file. name=%s, length=%d, mime=%s',
        filename,
        file.content_length,
        mime,
    )

    buffer = read_buffer(file)
    hash = hash_buffer(buffer)

    if hash_exists(hash):
        # Return the existing entry instead of writing a new file.
        file = File.get(File.hash == hash)

        return jsonify({
            **file.to_dict(),
            'deduplicated': True,
        })
    else:
        # Save the file into the filesystem if necessary.
        write_file(hash, buffer)

    file_id = generate_name(5)

    file = File.create(
        id=file_id,
        name=file.filename,
        hash=hash,
        mime=mime,
    )

    return jsonify(file.to_dict())
