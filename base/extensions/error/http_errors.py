from flask import render_template


def handle_bad_request(e):
    error = {'message': 'bad request!', 'code': e.code}
    return render_template('error.html', error=error), e.code


def handle_not_found(e):
    error = {'message': 'not found!', 'code': e.code}
    return render_template('error.html', error=error), e.code


def init_app(app):
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(404, handle_not_found)
