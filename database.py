# -*- coding: utf-8 -*-
import os
from elasticsearch import Elasticsearch
from flask.ext.pymongo import PyMongo

mongo = PyMongo()
es = Elasticsearch([os.getenv('BONSAI_URL')])