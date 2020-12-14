"""
Содержит настроенное приложение админки. Может запустить его в режиме разработки
"""

import flask_admin as fl_admin
from flask import Flask

from admin_panel.extensions import db
from admin_panel.login import init_login
from admin_panel.models import Sections, Queries, Quizzes, Tests, Profiles
from admin_panel.router import blueprint
from admin_panel.veiws.admin import MyAdminIndexView, ModelViewExcludeID, UserView
from core.config import settings

app = Flask(__name__, )
app = init_login(app)

app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['MONGODB_SETTINGS'] = settings.MONGODB_ADMIN

db.init_app(app)

app.register_blueprint(blueprint)

# Создаём админ панель во Flask-Admin
admin = fl_admin.Admin(app, index_view=MyAdminIndexView(url='/admin/panel'))

# Добавляем вьюхи представления данных
admin.add_view(UserView(Profiles, name="Пользователи"))
admin.add_view(ModelViewExcludeID(Tests, name="АвтоТесты"))

admin.add_view(ModelViewExcludeID(Queries, name="Логи запросов"))
admin.add_view(ModelViewExcludeID(Sections, name="Список тем"))
admin.add_view(ModelViewExcludeID(Quizzes, name="Викторины"))


# Чтобы запустить в тестовом режиме при разработке
if __name__ == "__main__":
    app.run(debug=True)
