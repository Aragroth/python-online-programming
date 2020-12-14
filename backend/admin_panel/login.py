from wtforms import form, fields, validators

# Define login and registration forms (for flask-login)
from admin_panel.models import Profiles
import flask_login as fl_login

from core.security import check_password
from loguru import logger

logger.add("log/password.log")


class LoginForm(form.Form):
    """Обрабатывает форму входа в админ панель"""
    username = fields.StringField(validators=[validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])

    def validate_username(self, field):
        """Только пользователя с именем admin может зайти"""
        user = self.get_user()
        print(user, flush=True)

        if user is None or user.username != 'admin':
            raise validators.ValidationError('Invalid user')

        if not check_password(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        print(self.username.data, flush=True)
        return Profiles.objects(username=self.username.data).first()


class RegistrationForm(form.Form):
    """Обрабатывает Регистрацию пользователя в админ панели (не поддерживается, но полезно)"""
    username = fields.StringField(validators=[validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])

    def validate_username(self, field):
        if Profiles.objects(username=self.username.data):
            raise validators.ValidationError('Duplicate username')


# Initialize flask-login
def init_login(app):
    login_manager = fl_login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return Profiles.objects(username=user_id).first()

    return app
