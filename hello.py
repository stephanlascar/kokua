import os
from elasticsearch import Elasticsearch
from flask import Flask, request
from geoip import geolite2


es = Elasticsearch([os.getenv('BONSAI_URL')])
app = Flask(__name__)


@app.before_first_request
def create_indexes():
    es.indices.create(index='sauron')


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

if __name__ == '__main__':
    app.run(debug=True)
