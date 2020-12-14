import flask_admin as fl_admin
import flask_login as fl_login
from flask_admin.contrib.mongoengine import ModelView

from admin_panel.veiws.utils import TemplateMixin


# Create customized model view class
class UserView(ModelView, TemplateMixin):
    form_excluded_columns = ('id')

    column_exclude_list = ['id', 'password']
    column_labels = {
        'username': 'Никнейм пользователя',
        'full_name': 'Имя пользователя',
        'email': 'Почта пользователя',
        'password': 'Хэш пароля',
        'title': 'Полное название',
    }


class QuizModelView(ModelView, TemplateMixin):
    form_labels = {
        "content": "cont12121221"
    }

    column_labels = {
        'short_title': 'Короткое название',
        'group': 'Группа заданий',
        'title': 'Полное название',
    }

    def is_accessible(self):
        return fl_login.current_user.is_authenticated


class MyModelView(ModelView, TemplateMixin):
    form_labels = {
        "content": "cont12121221"
    }

    column_labels = {
        'short_title': 'Короткое название',
        'group': 'Группа заданий',
        'title': 'Полное название',
    }

    def is_accessible(self):
        return fl_login.current_user.is_authenticated


class ModelViewExcludeID(ModelView, TemplateMixin):
    form_excluded_columns = ('id')

    column_exclude_list = ['id', ]
    column_labels = {
        'short_title': 'Короткое название',
        'group': 'Группа заданий',
        'title': 'Полное название',
    }

    def is_accessible(self):
        return fl_login.current_user.is_authenticated


# Create customized index view class
class MyAdminIndexView(fl_admin.AdminIndexView, TemplateMixin):

    def is_accessible(self):
        return fl_login.current_user.is_authenticated
