from datetime import datetime

from peewee import CharField, TextField, IntegerField, PrimaryKeyField, DateTimeField
from .base import BaseModel


class Word(BaseModel):
    id = PrimaryKeyField()
    heading = CharField(max_length=128)
    normalized_heading = CharField(max_length=128, null=True)
    translation = CharField(max_length=128)
    sound_name = TextField(null=True)
    requested_count = IntegerField(default=0)
    last_requested_date = DateTimeField(default=lambda: datetime.now())

    @staticmethod
    def is_one_word(word):
        if not len(word.split()) == 1:
            return False
        return True

    @staticmethod
    def is_camel_case(word):
        has_upper = 0
        for s in word:
            if s.isupper():
                has_upper += 1
            if has_upper > 1:
                return True
        return False

    def update_requested_count(self):
        self.requested_count += 1
