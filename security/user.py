# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin


class User(UserMixin):

    def __init__(self, _id, email, _type):
        self.email = email
        self.type = _type
        self.id = _id
