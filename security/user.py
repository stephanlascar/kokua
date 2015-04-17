# -*- coding: utf-8 -*-
from flask.ext.login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):

    def __init__(self, js_id, email):
        self.email = email
        self.js_id = js_id

    def is_authenticated(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.js_id
