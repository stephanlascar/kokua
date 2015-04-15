# -*- coding: utf-8 -*-
import os
from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, redirect, url_for
from geoip import geolite2
from form.chat_login_form import ChatLoginForm


es = Elasticsearch([os.getenv('BONSAI_URL')])
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/kokua.js')
def get_kokua_javascript():
    return render_template('javascript/kokua.js')


@app.route('/livechat.html', methods=('GET', 'POST'))
def livechat():
    form = ChatLoginForm()
    if form.validate():
        return redirect(url_for('chat2'))
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
