from admin_panel.extensions import db
from admin_panel.models.section import Sections
from admin_panel.models.utils import generate_uuid


class Answers(db.EmbeddedDocument):
    """Варинат ответа на вопрос"""
    id = db.DecimalField()
    answer = db.StringField(max_length=120)


class Questions(db.EmbeddedDocument):
    """Сам вопрос, варианты его ответов и правильные ответ"""
    question = db.StringField(max_length=120)
    answers = db.ListField(db.EmbeddedDocumentField(Answers))
    correct_answer = db.DecimalField()


class Quizzes(db.Document):
    """Само задание "опросник", содержит список вопросов, а также название раздела"""
    id = db.StringField(primary_key=True, default=generate_uuid)
    title = db.StringField(max_length=150, unique=True)
    section_name = db.ReferenceField(Sections, reverse_delete_rule=db.CASCADE)

    content = db.ListField(db.EmbeddedDocumentField(Questions))

    meta = {'db_alias': 'TestSystem', 'strict': False}

    def __str__(self):
        return self.title
