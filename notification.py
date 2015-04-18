# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, jsonify, current_app
from flask.ext.login import current_user

from pusher import pusher_from_url


pusher = pusher_from_url(os.getenv('PUSHER_URL'))
notification = Blueprint('pusher', __name__, template_folder='templates')


@notification.route('/pusher/auth', methods=['POST'])
def auth():
    channel_name = request.form['channel_name']
    socket_id = request.form['socket_id']

    return jsonify(pusher[channel_name].authenticate(socket_id, dict(email=current_user.email, user_id=str(current_user.id))))


@notification.route('/pusher/presence', methods=['POST'])
def presence():
    current_app.logger.info(request.json)
    return ''