# -*- coding: utf-8 -*-
import os
from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, redirect, url_for
from flask.ext.login import LoginManager, login_user
from geoip import geolite2
from form.chat_login_form import ChatLoginForm
from security.user import User


es = Elasticsearch([os.getenv('BONSAI_URL')])
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.getenv('SECRET_KEY', 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(js_id):
    return {}


@app.route('/kokua.js')
def get_kokua_javascript():
    return render_template('javascript/kokua.js')


@app.route('/test.html')
def test():
    return 'okokok'


@app.route('/livechat.html', methods=('GET', 'POST'))
def livechat():
    form = ChatLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(User(js_id=form.js_id, email=form.email))
            return redirect(url_for('test'))
    else:
        form.js_id.data = request.args['js_id']
    return render_template('livechat.html', form=form)


@app.route('/sauron', methods=['POST'])
def sauron():
    params = request.json
    localization = geolite2.lookup(request.remote_addr)
    params['ip'] = request.remote_addr
    params['user_agent'] = dict(header=request.user_agent.to_header(),
                                browser=request.user_agent.browser,
                                language=request.user_agent.language or 'fr',
                                platform=request.user_agent.platform,
                                version=request.user_agent.version)
    params['localization'] = localization.to_dict() if localization else dict()
    es.index(index='sauron', doc_type='surfer_events', body=params)
    return '', 200
