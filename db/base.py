from peewee import *
import datetime

import config


class BaseModel(Model):
    class Meta:
        database = config.DB
