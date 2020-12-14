from admin_panel.extensions import db
from admin_panel.models.utils import generate_uuid


class Sections(db.Document):
    """Задаёт 'тему' к которой могут относиться основные задания"""
    id = db.StringField(primary_key=True, default=generate_uuid)
    section_name = db.StringField(max_length=80)

    # noinspection PyRedeclaration
    meta = {'db_alias': 'TestSystem'}

    def __str__(self):
        return self.section_name
