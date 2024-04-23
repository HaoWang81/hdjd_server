# 铸铁毛坯生产监控
import datetime
import json
import logging

import pandas as pd
from flask import Blueprint, request, jsonify

from utils.db import MySQLClient

api_screen = Blueprint('api_screen', __name__)

ngc_sql_constants = {
    "表格": "select changhao,zaoxingzhixin,hexiang,kaixiangqingli,damo,rechuli,jingxiu,maopijianyan,tuzhuang, jiagong,jiagongjianyan from t_hdjd_product_monitor where  DATE_FORMAT(update_time, '%Y-%m-%d')=CURDATE() and (zaoxingzhixin<0 or hexiang <0 or kaixiangqingli<0 or damo<0 or rechuli<0 or  jingxiu < 0 or maopijianyan < 0 or tuzhuang<0 or  jiagong <0 or jiagongjianyan<0) ",
    "ngc欠数": """
    select DATE_FORMAT(t1.date, '%Y-%m-%d'),ifnull(t.sum_num,0) from (
SELECT IFNULL(ABS(SUM(zaoxingzhixin)), 0) AS sum_num, DATE_FORMAT(update_time, '%Y-%m-%d') as update_time
      FROM t_hdjd_product_monitor
      WHERE zaoxingzhixin < 0
        AND changhao LIKE '%NGC%'
        and count_flag='1'
        AND update_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 6 DAY) AND CURDATE() + INTERVAL 1 DAY - INTERVAL 1 SECOND group by t_hdjd_product_monitor.update_time) t right join (

SELECT DATE_SUB(CURDATE(), INTERVAL 6 DAY) AS date
UNION ALL
SELECT DATE_SUB(CURDATE(), INTERVAL 5 DAY)
UNION ALL
SELECT DATE_SUB(CURDATE(), INTERVAL 4 DAY)
UNION ALL
SELECT DATE_SUB(CURDATE(), INTERVAL 3 DAY)
UNION ALL
SELECT DATE_SUB(CURDATE(), INTERVAL 2 DAY)
UNION ALL
SELECT DATE_SUB(CURDATE(), INTERVAL 1 DAY)
UNION ALL
SELECT CURDATE()
)  t1 on t.update_time=t1.date order by  date
    """
}

import numpy as np


@api_screen.route('/screen/ngc/chart', methods=['POST'])
def ngc_chart():
    data = request.json
    client = MySQLClient('hdjd')
    tables = client.query(ngc_sql_constants['表格'], None)
    charts = client.query(ngc_sql_constants['ngc欠数'], None)
    result_table = []
    result_charts = dict()
    for item in tables:
        result_table.append(np.array(item).tolist())
    y = []
    x = []
    for item in charts:
        x.append(item[0])
        y.append(str(item[1]))
    result_charts["x"] = x
    result_charts["y"] = y
    result = dict()
    result['table'] = result_table
    result['charts'] = result_charts
    return json.dumps(result, ensure_ascii=False)


card_sql_constants = {
    "大件数量":
        """
     select sum(check_num) 
from t_hdjd_blank_production
where per_weight > 5000
  and production_date  = %s
     """,
    "大件吨位":
        """
     select round(ifnull(sum(check_num * per_weight) / 1000, 0)) as product_weight
from t_hdjd_blank_production
where per_weight > 5000
  and production_date = %s
     """,
    "小件数量":
        """
select sum(check_num)
from t_hdjd_blank_production
where per_weight < 5000 and production_company = '本公司'
  and production_date = %s 
""",
    "小件吨位":
        """
select round(ifnull(sum(check_num * per_weight) / 1000, 0)) as product_weight
from t_hdjd_blank_production
where per_weight < 5000 and production_company = '本公司'
    # ngc造型吨位
  and production_date = %s
""",
    "ngc造型数量":
        """
        select sum(check_num)
   from t_hdjd_blank_production
   where LOWER(production_name) like '%ngc%'
     and production_date = %s
        """,
    "ngc造型吨位":
        """
        select round(ifnull(sum(check_num * per_weight) / 1000, 0)) as product_weight
        from t_hdjd_blank_production
        where LOWER(production_name) like '%ngc%'
          and production_date = %s
        """,
    "ngc欠缺数量": """
            select abs(sum(zaoxingzhixin))
        from t_hdjd_product_monitor
        where LOWER(changhao) like '%ngc%'
          and DATE_FORMAT(update_time, '%Y-%m-%d') = CURDATE() and zaoxingzhixin<0  and count_flag='1'
    """,

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
where per_weight < 5000 and production_company = '本公司'
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
where  LOWER(production_name) like '%ngc%'
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

    # dates = client.getWeekDateAreaByCurrent(date_str)

    result = dict()
    for key, value in card_sql_constants.items():
        if value is not None and len(value) > 0:
            rows = []
            if '%s' in value:
                rows = client.query(value, (date_str,))
            else:
                rows = client.query(value, None)
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


@api_screen.route('/screen/lv_monitor/', methods=['POST'])
def screen_lv_monitor():
    client = MySQLClient('hdjd')
    sql = f"""select changhao,
            jinrizaoxing,
            benzhouzaoxing,
            benyuezaoxingqianshu,
            jinrizhuanxu,
            benzhouzhuanxu,
            benyuezhuanxuqianshu,
            maopichengpin,
            damo,
            rechuli,
            jingxiu,
            maopizaizhi,
            jinrijiagong,
            benzhoujiagong,
            yuedujiagong,
            jiagongzaizhi,
            jinriqingli,
            benzhouqingli,
            yueduqingli,
            qinglizaizhi from t_hdjd_product_monitor_lv where  DATE_FORMAT(update_time, '%Y-%m-%d') = CURDATE() and (jinrizaoxing!=0 or benzhouzaoxing!=0 or damo!=0 or  rechuli!=0 or jingxiu!=0 or maopizaizhi!=0 or maopichengpin!=0 or jinrijiagong!=0 or benzhoujiagong!=0 or jiagongzaizhi!=0 or jinriqingli!=0 or benzhouqingli!=0 or qinglizaizhi!=0)"""
    result = client.query(sql, None)
    serialized_data = [list(item) for item in result]

    return json.dumps(serialized_data, ensure_ascii=False)
