from admin_panel.extensions import db
from .quiz import Quizzes
from .tests import Tests
from admin_panel.models.utils import UserMixin, generate_uuid
from core.security import hash_password


class CodeSnippets(db.EmbeddedDocument):
    """Хранение кода пользователя для конкретного задания"""
    test_id = db.ReferenceField(Tests)
    code = db.StringField()


class Profiles(db.Document, UserMixin):
    """Данные авторизации пользователя, а также список пройденных им заданий, плюс их код"""
    id = db.StringField(primary_key=True, default=generate_uuid)
    username = db.StringField(max_length=80, unique=True)
    password = db.StringField(max_length=64)

    full_name = db.StringField(max_length=200)
    email = db.StringField(max_length=200)

    snippets = db.ListField(db.EmbeddedDocumentField(CodeSnippets))
    passed_tests = db.ListField(db.ReferenceField(Tests, reverse_delete_rule=db.PULL))
    passed_quizzes = db.ListField(db.ReferenceField(Quizzes, reverse_delete_rule=db.PULL))
    last_task = db.ReferenceField(Tests, reverse_delete_rule=db.NULLIFY, null=True)

    # noinspection PyRedeclaration
    meta = {'db_alias': 'users', 'strict': False}

    def save(self):
        """Добавляем хеширование пароля, при его изменении через админку"""
        maybe_user = Profiles.objects(username=self.username).first()
        if not self.id or maybe_user is None or maybe_user.password != self.password:
            self.password = hash_password(self.password)

        return super().save()

    def __str__(self):
        return str(self.username)
