__all__ = ['password_required']

import functools

from flask import current_app, jsonify, request


def password_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        password = request.headers.get('Authorization')

        if not password:
            return jsonify(error='authorization required'), 401

        needed = current_app.config['PASSWORD']

        if password != needed:
            return jsonify(error='invalid password'), 401

        return f(*args, **kwargs)
    return wrapped
