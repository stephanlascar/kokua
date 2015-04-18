# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, request, render_template, redirect, current_app, url_for
from flask.ext.login import login_user, current_user
from database import mongo, es
from form.chat_login_form import ChatLoginForm
from security.user import User


livechat = Blueprint('livechat', __name__, template_folder='templates')


@livechat.route('/livechat/login.html', methods=('GET', 'POST'))
def login():
    form = ChatLoginForm()
    if form.validate_on_submit():
        mongo.db.users.update({'email': form.email.data, 'role': 'visitor'}, {'$addToSet': {'js_id': form.js_id.data}}, upsert=True)
        mongo_user = mongo.db.users.find_one({'email': form.email.data, 'role': 'visitor'})
        login_user(User(mongo_user['_id'], form.email.data, 'visitor'), remember=True)
        es.index(index='sauron', doc_type='conversations', body={
            'datetime': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'from': form.email.data,
            'message': form.message.data
        })
        current_app.logger.info(mongo_user)
        return redirect('livechat/index.html')
    form.js_id.data = request.args['js_id']
    return render_template('livechat/login.html', form=form)


@livechat.route('/livechat/index.html')
def index():
    if current_user.is_authenticated():
        previous_conversations = es.search(index='sauron', doc_type='conversations', q='from:{email}'.format(email=current_user.email))
        return render_template('livechat/index.html', previous_conversations=previous_conversations)
    else:
        return redirect(url_for('livechat.login'))