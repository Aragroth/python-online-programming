from admin_panel.extensions import db
from admin_panel.models import Sections
from admin_panel.models.utils import generate_uuid


class TestData(db.EmbeddedDocument):
    """Содержит, что должно быть передано программе и что она должна вывести"""
    input = db.StringField()
    output = db.StringField()
    is_answer_empty = db.BooleanField()


class Tests(db.Document):
    """
    Задание тестирующей системы. Содержит открытые и закрытые тесты, а также описание
    и при необходимости дополнительную фотографию. Краткое название отображается в сайдбаре
    """
    id = db.StringField(primary_key=True, default=generate_uuid)
    section_name = db.ReferenceField(Sections, unique=False, reverse_delete_rule=db.CASCADE)
    title = db.StringField(max_length=150)
    short_title = db.StringField(max_length=60)
    description = db.StringField()
    photo = db.ImageField(db_alias='files')

    examples = db.ListField(db.EmbeddedDocumentField(TestData))
    real_tests = db.ListField(db.EmbeddedDocumentField(TestData))

    meta = {'db_alias': 'TestSystem', 'strict': False}

    def save(self):
        """Переобределяем метод сохранения модели, чтобы избавиться от лишних символов переноса"""
        for i in range(len(self.examples)):
            self.examples[i].output = self.examples[i].output.replace('\r', '', -1)
            self.examples[i].input = self.examples[i].input.replace('\r', '', -1)

        for i in range(len(self.real_tests)):
            self.real_tests[i].output = self.real_tests[i].output.replace('\r', '', -1)
            self.real_tests[i].input = self.real_tests[i].input.replace('\r', '', -1)

        return super().save()

    def __str__(self):
        return self.short_title
