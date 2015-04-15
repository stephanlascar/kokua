# -*- coding: utf-8 -*-
from wtforms import Form, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class ChatLoginForm(Form):

    email = EmailField('Introduce yourself', validators=[DataRequired()])
    message = StringField('Message', widget=TextArea(), validators=[DataRequired()])
