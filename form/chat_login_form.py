# -*- coding: utf-8 -*-
from wtforms import StringField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from flask_wtf import Form


class ChatLoginForm(Form):

    email = EmailField('Introduce yourself', validators=[DataRequired()])
    message = StringField('Message', widget=TextArea(), validators=[DataRequired()])
    js_id = HiddenField()

