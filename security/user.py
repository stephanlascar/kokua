# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin


class User(UserMixin):

    def __init__(self, js_id, email):
        self.email = email
        self.js_id = js_id

    def get_id(self):
        return self.js_id
