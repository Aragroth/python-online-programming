from admin_panel.extensions import db
from .tests import Tests
from admin_panel.models.profile import Profiles
from admin_panel.models.utils import generate_uuid

STATUS = [
    'accepted',
    'running',
    'finished',
]


class Queries(db.Document):
    """Информация для логирования запусков тестов над программой пользователя"""
    id = db.StringField(primary_key=True, default=generate_uuid)
    task = db.ReferenceField(Tests, reverse_delete_rule=db.CASCADE)
    timestamp = db.DateTimeField()
    status = db.StringField(choices=STATUS)
    username = db.ReferenceField(Profiles, reverse_delete_rule=db.CASCADE)
    passed_all = db.BooleanField(null=True)
    percent_passed = db.IntField(null=True)
    sample_test = db.BooleanField(null=True)

    # noinspection PyRedeclaration
    meta = {'db_alias': 'TestSystem', 'strict': False}
