# -*- coding: utf-8 -*-
from bson import ObjectId
from flask.ext.login import LoginManager
from database import mongo
from security.user import User


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    mongo_user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(mongo_user['_id'], mongo_user['email'], mongo_user['role'])