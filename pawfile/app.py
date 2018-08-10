import os

from flask import Flask, request, jsonify, send_file

from .decorators import password_required
from .db import db
from .models import File
from .name import generate_name
from .upload import handle_upload

app = Flask(__name__)
app.config.from_object('pawfile.config')

if 'CONFIG' in os.environ:
    app.config.from_envvar('CONFIG')


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route('/<file_id>', methods=['GET'])
def view(file_id):
    try:
        file = File.get(File.id == file_id)

        path = os.path.join(
            app.config['UPLOADED_FILES'],
            file.hash,
        )

        return send_file(
            filename_or_fp=path,
            as_attachment=True,
            attachment_filename=file.name,
        )
    except File.DoesNotExist:
        return '', 404


@app.route('/', methods=['POST'])
@password_required
def upload():
    if 'file' not in request.files:
        return jsonify(error='no file provided'), 400

    file = request.files['file']

    app.logger.info(
        'Creating file. name=%s, length=%d, mime=%s',
        file.filename,
        file.content_length,
        file.content_type,
    )

    # Save the file into the filesystem if necessary by its SHA256 hash.
    hash, already_exists = handle_upload(file)

    if not already_exists:
        # Return the existing entry.
        file = File.get(File.hash == hash)

        return jsonify({
            **file.to_dict(),
            'existing': True
        })

    file_id = generate_name(5)

    file = File.create(
        id=file_id,
        name=file.filename,
        hash=hash,
    )

    return jsonify(file.to_dict())
