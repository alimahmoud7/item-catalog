from .models.user_helper import get_user_info

from flask import Flask, jsonify

from flask_wtf.csrf import CSRFProtect, CSRFError


app = Flask(__name__)

# Implement CSRF protection
csrf = CSRFProtect(app)

# Configurations
app.config.from_object('config')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    """Handling CSRF Error"""
    return jsonify(error={'msg': e.description}), 400


# To use this function in templates
app.jinja_env.globals['user_info'] = get_user_info


# Import modules using its blueprint handler variable
from app.views import *  # noqa

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(field)
app.register_blueprint(mooc)
