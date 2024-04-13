# 铸铁毛坯生产监控
import logging

import openpyxl
import pandas as pd
from flask import Blueprint, request, jsonify

from utils.db import  MySQLClient

api_screen = Blueprint('api_screen', __name__)


@api_screen.route('/screen/fresh', methods=['POST'])
def fresh():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    # file.save("生产监控.xlsx")

    # wb = openpyxl.load_workbook(filename=file, read_only=True, data_only=True, keep_links=False,
    #                             keep_vba=False)
    # # 获取第一个工作表
    # ws = wb.active
    # print(ws)
    #
    pd.set_option('display.max_columns', None)
    df = pd.read_excel(file, sheet_name="毛坯生产数量1")
    data = []

    for index, row in df.iterrows():
        production_date = ''
        try:
            # pd.to_datetime(row[0])
            date = pd.to_datetime(row[0], origin='1899-12-30', unit='D', errors='raise', infer_datetime_format=False,
                                  exact=True, cache=False, utc=None, format=None)
            production_date = date
        except Exception as e:
            logging.error('非日期格式')
        data.append((row[1], row[2], row[3], row[5], row[9], production_date))
    client = MySQLClient('hdjd')
    insert_sql = "insert into t_hdjd_blank_production(production_name,check_num,per_weight,production_company,production_unit,production_date) values(%s,%s,%s,%s,%s,%s) "
    client.insert_batch(insert_sql, data)
    result = client.query('select * from t_hdjd_blank_production')
    print(result)
    return "None"
