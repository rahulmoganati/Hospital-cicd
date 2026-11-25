from functools import wraps
from flask import abort
from flask_login import current_user, login_required
def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapped(*args, **kwargs):
            if current_user.role not in roles: abort(403)
            return fn(*args, **kwargs)
        return wrapped
    return decorator
