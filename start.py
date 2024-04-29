# -*- coding: utf-8 -*-
import json

import os.path
import sys
import threading

import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from utils.db import MySQLClient
from utils.scheduleUtil import my_task

sys.path.append(os.path.abspath("util"))
from io import BytesIO

from flask import Flask, request, jsonify, send_file, render_template, redirect
import pandas as pd

from util import readExcle, buildHtml
from flask_cors import CORS

from utils.init import config

logger.add("./hdjd.log", rotation="500 MB", level="DEBUG")

app = Flask(__name__, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 10MB

CORS(app)


@app.before_request
def before_request():
    client = MySQLClient('hdjd')
    client.insert(f'insert into t_hdjd_log(ip,url) values (%s,%s)',
                  (request.headers.get('X-Forwarded-For'), request.url))


@app.route('/hdjd/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    file.save("生产监控.xlsx")
    result = readExcle("生产监控.xlsx")
    buildHtml(result)
    # 在这里你可以定义文件保存的路径和其他逻辑
    # 例如：file.save('/path/to/save/' + secure_filename(file.filename))

    return jsonify({'message': 'File uploaded successfully'})


@app.route('/hdjd/fresh', methods=['POST'])
def fresh():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    file.save("生产监控.xlsx")
    # result = readExcle("生产监控.xlsx")
    # buildHtml(result)
    # 在这里你可以定义文件保存的路径和其他逻辑
    # 例如：file.save('/path/to/save/' + secure_filename(file.filename))

    return "刷新成功！"


@app.route('/hdjd/download_excel', methods=['GET'])
def download_excel():
    # 创建一个示例的DataFrame
    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35]}
    df = pd.DataFrame(data)

    # 将DataFrame写入BytesIO对象中，以便在内存中创建Excel文件
    excel_data = BytesIO()
    df.to_excel(excel_data, index=False)

    # 将BytesIO对象的指针移到文件的开头
    excel_data.seek(0)

    # 设置HTTP响应头，指定文件类型和文件名
    headers = {
        'Content-Disposition': 'attachment; filename=生产监控.xlsx',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }

    # 将Excel文件作为响应返回给客户端
    return send_file(excel_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     download_name="生产监控.xlsx",
                     as_attachment=True)


@app.route('/hdjd/read_excle_screen', methods=['POST'])
def read_excel_screen():
    client = MySQLClient('hdjd')
    tables = client.query(ngc_sql_constants['表格'], None)
    result_table = []
    for item in tables:
        result_table.append(np.array(item).tolist())
    return json.dumps(result_table, ensure_ascii=False)


@app.route('/hdjd/upload')
def upload():
    return render_template('upload.html')


@app.route('/screen')
def screen():
    return redirect('http://www.laotianshi.top/#/screen/tie_monitor')


@app.route('/ngc_monitor')
def ngc_monitor():
    return render_template('screen.html')


from api.api_screen import api_screen, ngc_sql_constants
from api.api_settings import api_settings
from api.api_home import api_home


def start_schedule():
    # 创建一个调度器实例
    logger.info('创建一个调度器实例')
    scheduler = BlockingScheduler()
    # 添加任务，每天凌晨12点执行
    scheduler.add_job(my_task, 'cron', hour=1, minute=6)

    # 启动调度器
    try:
        scheduler.start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    logger.info('...启动服务...')
    app.register_blueprint(api_screen)
    app.register_blueprint(api_settings)
    app.register_blueprint(api_home)
    schedule_thread = threading.Thread(target=start_schedule)
    schedule_thread.start()
    app.run(host="0.0.0.0", port=config['server']['port'])
