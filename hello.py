# -*- coding: utf-8 -*-
import os
import datetime
from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, redirect, url_for
from flask.ext.login import login_user, login_required
from geoip import geolite2
from form.chat_login_form import ChatLoginForm
from livechat import livechat
from security.user import AnonymousUser


#es = Elasticsearch([os.getenv('BONSAI_URL')])
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.getenv('SECRET_KEY', 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')


app.register_blueprint(livechat)


@app.route('/kokua.js')
def get_kokua_javascript():
    return render_template('javascript/kokua.js')


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
    #es.index(index='sauron', doc_type='surfer_events', body=params)
    return '', 200
