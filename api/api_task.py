import json

from flask import Blueprint, request

from utils.db import MySQLClient

api_task = Blueprint('api_task', __name__)


@api_task.route('/task/save', methods=['POST'])
def save():
    request_data = request.json
    return json.dumps([], ensure_ascii=False)
