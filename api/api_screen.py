# 铸铁毛坯生产监控
import json
import logging

import openpyxl
import pandas as pd
from flask import Blueprint, request, jsonify

from utils.db import MySQLClient

api_screen = Blueprint('api_screen', __name__)


@api_screen.route('/screen/fresh', methods=['POST'])
def fresh():
    client = MySQLClient('hdjd')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    pd.set_option('display.max_columns', None)
    df = pd.read_excel(file, sheet_name="毛坯生产数量1")
    data = []

    for index, row in df.iterrows():
        production_date = ''
        try:
            date = pd.to_datetime(row[0], origin='1899-12-30', unit='D', errors='raise', infer_datetime_format=False,
                                  exact=True, cache=False, utc=None, format=None)
            production_date = date
        except Exception as e:
            logging.error(f'非日期格式,{e}')
        data.append((row[1], row[2], row[3], row[5], row[9], production_date))
    insert_sql = "insert into t_hdjd_blank_production(production_name,check_num,per_weight,production_company,production_unit,production_date) values(%s,%s,%s,%s,%s,%s) "
    client.delete("delete from t_hdjd_blank_production ", None)
    client.insert_batch(insert_sql, data)
    return "None"

    # 大件数量
    # 大件吨位

    # 小件数量
    # 小件吨位

    # ngc造型数量
    # ngc造型吨位
    # ngc欠缺数量


card_sql_constants = {
    "大件数量":
        """
     select sum(check_num)
from t_hdjd_blank_production
where per_weight > 5000
  and production_date between %s and %s
     """,
    "大件吨位":
        """
     select round(ifnull(sum(check_num * per_weight) / 1000, 0)) as product_weight
from t_hdjd_blank_production
where per_weight > 5000
  and production_date between %s and %s
     """,
    "小件数量":
        """
select sum(check_num)
from t_hdjd_blank_production
where per_weight < 5000
  and production_date between  %s and %s
""",
    "小件吨位":
        """
select round(ifnull(sum(check_num * per_weight) / 1000, 0)) as product_weight
from t_hdjd_blank_production
where per_weight < 5000
  and production_date between %s and %s
""",
    "ngc造型数量":
        """
        select sum(check_num)
   from t_hdjd_blank_production
   where LOWER(production_name) like '%ngc%'
     and production_date between %s and %s
        """,
    "ngc造型吨位":
        """
        select round(ifnull(sum(check_num * per_weight) / 1000, 0)) as product_weight
        from t_hdjd_blank_production
        where LOWER(production_name) like '%ngc%'
          and production_date between %s and %s
        """,
    "ngc欠缺数量": None,

}

chart_sql_constants = {
    "大件数量周统计": """
    select b.week_num, b.week_name, ifnull(a.check_num,0)
from (
    select production_date,(CASE WEEKDAY(production_date)
        WHEN 0 THEN '周一'
        WHEN 1 THEN '周二'
        WHEN 2 THEN '周三'
        WHEN 3 THEN '周四'
        WHEN 4 THEN '周五'
        WHEN 5 THEN '周六'
        WHEN 6 THEN '周日'
    END ) AS day_of_week,sum(check_num) as check_num
from t_hdjd_blank_production
where per_weight >= 5000
  and production_date between %s and %s  group by production_date
  ) a
         right join t_hdjd_code_weeknum b on b.week_name = a.day_of_week order by week_num
    """,
    "小件数量周统计": """
        select b.week_num, b.week_name, ifnull(a.check_num,0)
from (
     select production_date,(CASE WEEKDAY(production_date)
        WHEN 0 THEN '周一'
        WHEN 1 THEN '周二'
        WHEN 2 THEN '周三'
        WHEN 3 THEN '周四'
        WHEN 4 THEN '周五'
        WHEN 5 THEN '周六'
        WHEN 6 THEN '周日'
    END ) AS day_of_week,sum(check_num) as check_num
from t_hdjd_blank_production
where per_weight < 5000
  and production_date between %s and %s  group by production_date
    ) a
         right join t_hdjd_code_weeknum b on b.week_name = a.day_of_week order by  b.week_num
    """,
    "ngc数量周统计": """
        select b.week_num, b.week_name, ifnull(a.check_num,0)
from (
     select production_date,(CASE WEEKDAY(production_date)
        WHEN 0 THEN '周一'
        WHEN 1 THEN '周二'
        WHEN 2 THEN '周三'
        WHEN 3 THEN '周四'
        WHEN 4 THEN '周五'
        WHEN 5 THEN '周六'
        WHEN 6 THEN '周日'
    END ) AS day_of_week,sum(check_num) as check_num
from t_hdjd_blank_production
where per_weight > 5000 and LOWER(production_name) like '%ngc%'
  and production_date between %s and %s  group by production_date 
    ) a
         right join t_hdjd_code_weeknum b on b.week_name = a.day_of_week order by b.week_num
    """,
    # "ngc欠缺周统计": "",
    # "表格": ""
}


@api_screen.route('/screen/card', methods=['POST'])
def screen_card():
    client = MySQLClient('hdjd')
    data = request.json
    if data is None:
        data = {}
    date_str = data.get('date_str', '')

    dates = client.getWeekDateAreaByCurrent(date_str)

    result = dict()
    for key, value in card_sql_constants.items():
        if value is not None and len(value) > 0:
            rows = client.query(value, (dates[0], dates[1]))
            if len(rows) > 0 and rows[0][0] is not None:
                result[key] = str(rows[0][0])
            else:
                result[key] = '0'
        else:
            result[key] = '0'
    return json.dumps(result, ensure_ascii=False)


# 大件数量周对比
@api_screen.route('/screen/chart/highWeight', methods=['POST'])
def screen_highWeight():
    client = MySQLClient('hdjd')
    data = request.json
    if data is None:
        data = {}
    date_str = data.get('date_str', '')
    dates = client.getWeekDateAreaByCurrent(date_str)
    lastDates = client.getLastWeekDateAreaByCurrent(date_str)
    result = dict({
        "大件数量周统计": {
            "本周": [],
            "上周": []
        },
        "小件数量周统计": {
            "本周": [],
            "上周": []
        },
        "ngc数量周统计": {
            "本周": [],
            "上周": []
        }
    })
    for key, value in chart_sql_constants.items():
        week_rows = client.query(value, (dates[0], dates[1]))
        last_week_rows = client.query(value, (lastDates[0], lastDates[1]))
        result[key]['本周'] = []
        for row in week_rows:
            result[key]['本周'].append(str(row[2]))
        for row in last_week_rows:
            result[key]['上周'].append(str(row[2]))
    return json.dumps(result, ensure_ascii=False)
