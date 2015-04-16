# -*- coding: utf-8 -*-
import os
import datetime
from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, redirect, url_for
from flask.ext.login import LoginManager, login_user, login_required
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
    result = es.search(index='sauron', doc_type='surfer_emails',
                       body={'size': 1,
                             'query': {'filtered': {'filter': {'term': {'js_id': js_id}}}},
                             'sort': {'datetime': {'order': 'desc'}}})
    return User(js_id=js_id, email=result['hits']['hits'][0]['_source']['email'])


@app.route('/kokua.js')
def get_kokua_javascript():
    return render_template('javascript/kokua.js')


@app.route('/test.html')
@login_required
def test():
    return 'okokok'


@app.route('/livechat.html', methods=('GET', 'POST'))
def livechat():
    form = ChatLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            es.index(index='sauron', doc_type='surfer_emails', body=dict(js_id=form.js_id.data, email=form.email.data, datetime=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
            login_user(User(js_id=form.js_id.data, email=form.email.data))
            return redirect(url_for('test'))
    else:
        form.js_id.data = request.args['js_id']
    return render_template('livechat.html', form=form)


@app.route('/sauron', methods=['POST'])
def sauron():
    params = request.json
    localization = geolite2.lookup(request.remote_addr)
    params['datetime'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    params['ip'] = request.remote_addr
    params['user_agent'] = dict(header=request.user_agent.to_header(),
                                browser=request.user_agent.browser,
                                language=request.user_agent.language or 'fr',
                                platform=request.user_agent.platform,
                                version=request.user_agent.version)
    params['localization'] = localization.to_dict() if localization else dict()
    es.index(index='sauron', doc_type='surfer_events', body=params)
    return '', 200
