import uuid


class UserMixin:
    """
    Flask-Login integration
    NOTE: is_authenticated, is_active, and is_anonymous
    are methods in Flask-Login < 0.3.0
    """
    def __init__(self):
        self.username = None
        self.authenticated = None

    def is_active(self):
        """True, потому что все пользователи по-умолчанию 'рабочие'"""
        return True

    def get_id(self):
        """Необходимо вернуть имя пользователя, т.к. это нужно для Flask-Login"""
        return self.username

    def is_authenticated(self):
        """Возвращает True, если пользователь авторизован"""
        return self.authenticated

    def is_anonymous(self):
        """False, поскольку анонимные пользователи не поддерживаются"""
        return False

    # Требуется для отображения во Flask-Admin
    def __unicode__(self):
        return self.username


def generate_uuid():
    """Генерирует уникальный идентификатор"""
    return str(uuid.uuid4())
