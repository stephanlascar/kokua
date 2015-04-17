# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template
from form.chat_login_form import ChatLoginForm


livechat = Blueprint('livechat', __name__, template_folder='templates')


@livechat.route('/livechat.html', methods=('GET', 'POST'))
def index():
    form = ChatLoginForm()
    if form.validate_on_submit():
        return render_template('livechat/index.html', form=form)
    form.js_id.data = request.args['js_id']
    return render_template('livechat/login.html', form=form)