import json

from flask import Blueprint, request

from utils.db import MySQLClient

api_ai = Blueprint('api_ai', __name__)


@api_ai.route('sqlQuery', methods=['POST'])
def sqlQuery():
    sql = request.json.get('sql')
    client = MySQLClient("test")
    rows = client.query(sql, None)

    value = 0
    for row in rows:
        value = row[0]
    result = dict({
        "data": value,
        "code": 2000,
        "msg":"success"
    })
    return json.dumps(result, ensure_ascii=False)
