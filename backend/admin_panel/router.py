"""Public section, including homepage and signup."""

import flask_login as fl_login
from flask import (
    Blueprint, request, render_template, url_for, redirect
)

from admin_panel.login import LoginForm

blueprint = Blueprint("auth", __name__, url_prefix="/admin", static_folder="../static")


@blueprint.route('/')
def index():
    """Выводит основную страницу"""
    return render_template('index.html', user=fl_login.current_user)


@blueprint.route('/login', methods=('GET', 'POST'))
def login_view():
    """Выводит форму авторизации"""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        fl_login.login_user(user, remember=True)
        return redirect(url_for('auth.index'))

    return render_template('form.html', form=form)


# @blueprint.route('/register/', methods=('GET', 'POST'))
# def register_view():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = Profiles()
#
#         form.populate_obj(user)
#         user.save()
#
#         fl_login.login_user(user, remember=True)
#         return redirect(url_for('auth.index'))
#
#     return render_template('form.html', form=form)


@blueprint.route('/logout')
def logout_view():
    """Разлогинивает пользователя из админ панели"""
    fl_login.logout_user()
    return redirect(url_for('auth.index'))
