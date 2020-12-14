"""Является точкой запуска админской панели через gunicorn"""
from admin_panel.admin import app

if __name__ == "__main__":
    app.config['APPLICATION_ROOT'] = '/admin'
    app.run()
