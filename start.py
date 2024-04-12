# -*- coding: utf-8 -*-

from io import BytesIO

from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
from werkzeug.utils import secure_filename

from util import readExcle, buildHtml, readExcleByScreen
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')

CORS(app)


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
    return readExcleByScreen("生产监控.xlsx")


@app.route('/hdjd/upload')
def upload():
    return render_template('upload.html')


@app.route('/screen')
def screen():
    return render_template('screen.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
