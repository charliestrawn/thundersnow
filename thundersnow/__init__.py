import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

dev_config = 'thundersnow.config.DevelopmentConfig'
app_settings = os.getenv('APP_SETTINGS', dev_config)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from thundersnow.admin import admin_blueprint # NOQA E402
from thundersnow.api.auth import auth_blueprint # NOQA E402
from thundersnow.api.members import members_blueprint # NOQA E402
from thundersnow.api.payments import payments_blueprint # NOQA E402
from thundersnow.api.reports import reports_blueprint # NOQA E402
from thundersnow.api.users import users_blueprint # NOQA E402
from thundersnow.api.weeks import weeks_blueprint # NOQA E402

from thundersnow.models import Member # NOQA E402


app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(payments_blueprint, url_prefix='/api')
app.register_blueprint(members_blueprint, url_prefix='/api')
app.register_blueprint(reports_blueprint, url_prefix='/api')
app.register_blueprint(users_blueprint, url_prefix='/api')
app.register_blueprint(weeks_blueprint, url_prefix='/api')


@app.route('/')
def index():
    """
    Main route for serving the index page.
    """
    return app.send_static_file('index.html')
