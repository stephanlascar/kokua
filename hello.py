# -*- coding: utf-8 -*-
import os
import datetime
from flask import Flask, request, render_template
from geoip import geolite2
import pymongo
from database import mongo
from security import login_manager
from livechat import livechat
from notification import notification


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.getenv('SECRET_KEY', 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')
app.config['MONGO_URI'] = os.getenv('MONGOLAB_URI')


mongo.init_app(app)
login_manager.init_app(app)
app.register_blueprint(livechat)
app.register_blueprint(notification)


@app.before_first_request
def create_mongo_index():
    mongo.db.bookmarks.ensure_index([('user.email', pymongo.ASCENDING), ('role', pymongo.ASCENDING)], background=True, unique=True)


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
