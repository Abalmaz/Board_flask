from flask import redirect, session
from datetime import datetime, timedelta
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def check(times, counts):
    if session.get(times) is None or datetime.now() > session.get(times):
        session[times] = datetime.now() + timedelta(hours=1)
        session[counts] = 5
    if session[counts]:
        return True
    return False


def can_comments():
    return check("time_update_likes_count", "count_comments")


def can_likes():
    return check("time_update_likes_count", "count_likes")


def validator(form_input, json_data):
    errors = {}
    if json_data is None:
        errors['Error'] = "Request is empty"
    elif form_input == 'board':
        if json_data.get("board_name") is None:
            errors['board'] = "Board is required"
        elif len(json_data.get('board_name')) > 50:
            errors['board'] = "Board name is too long. Max 50 symbols."
    elif form_input == 'comment':
        if json_data.get("comment_text") is None:
            errors['comment'] = "Comment is required"
        elif len(json_data.get('comment')) > 255:
            errors['comment'] = "Comment is too long. Max 255 symbols."
    elif form_input == 'user':
        if json_data.get("username") is None:
            errors['user'] = "User name is required"
        elif len(json_data.get('username')) > 30:
            errors['user'] = "Username is too long. Max 30 symbols."


    return errors
