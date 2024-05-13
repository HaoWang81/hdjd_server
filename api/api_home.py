import json

from flask import Blueprint

from utils.db import MySQLClient

api_home = Blueprint('api_home', __name__)


@api_home.route('/home/lvCount', methods=['POST'])
def get_lvCount():
    sql = f"""
        select cast(t1.hour as signed ) hour,ifnull(t.sum,0) sum from (
        select DATE_FORMAT(update_time, '%H') hour, count(0) sum
        from t_hdjd_log
        where ip is not null
        and url = 'http://www.laotianshi.top/screen/lv_monitor/'
        and date_format(update_time, '%Y-%m-%d') = CURDATE()
        group by DATE_FORMAT(update_time, '%H') ) t right join  t_hdjd_code_hour t1 on t.hour=t1.hour order by  hour
    """
    client = MySQLClient("hdjd")
    rows = client.query(sql, None)
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
    result = dict({
        "x": x,
        "y": y
    })
    return json.dumps(result, ensure_ascii=False)


@api_home.route('/home/ngcCount', methods=['POST'])
def get_ngcCount():
    sql = f"""
        select cast(t1.hour as signed ) hour,ifnull(t.sum,0) sum from (
        select DATE_FORMAT(update_time, '%H') hour, count(0) sum
        from t_hdjd_log
        where ip is not null
        and url = 'http://www.laotianshi.top/screen'
        and date_format(update_time, '%Y-%m-%d') = CURDATE()
        group by DATE_FORMAT(update_time, '%H')  ) t right join  t_hdjd_code_hour t1 on t.hour=t1.hour order by  hour
    """
    client = MySQLClient("hdjd")
    rows = client.query(sql, None)
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
    result = dict({
        "x": x,
        "y": y
    })
    return json.dumps(result, ensure_ascii=False)


@api_home.route('/home/tieCount', methods=['POST'])
def get_tieCount():
    sql = f"""
        select cast(t1.hour as signed ) hour,ifnull(t.sum,0) sum from (
        select DATE_FORMAT(update_time, '%H') hour, count(0) sum
        from t_hdjd_log
        where ip is not null
        and url = 'http://www.laotianshi.top/screen/tie_monitor/'
        and date_format(update_time, '%Y-%m-%d') = CURDATE()
        group by DATE_FORMAT(update_time, '%H')  ) t right join  t_hdjd_code_hour t1 on t.hour=t1.hour order by  hour
    """
    client = MySQLClient("hdjd")
    rows = client.query(sql, None)
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
    result = dict({
        "x": x,
        "y": y
    })
    return json.dumps(result, ensure_ascii=False)

@api_home.route('/home/ngcInnerCount', methods=['POST'])
def get_ngcInnerCount():
    sql = f"""
        select cast(t1.hour as signed ) hour,ifnull(t.sum,0) sum from (
        select DATE_FORMAT(update_time, '%H') hour, count(0) sum
        from t_hdjd_log
        where ip is not null
        and url = 'http://www.laotianshi.top/screen/ngc_monitor/'
        and date_format(update_time, '%Y-%m-%d') = CURDATE()
        group by DATE_FORMAT(update_time, '%H')  ) t right join  t_hdjd_code_hour t1 on t.hour=t1.hour order by  hour
    """
    client = MySQLClient("hdjd")
    rows = client.query(sql, None)
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
    result = dict({
        "x": x,
        "y": y
    })
    return json.dumps(result, ensure_ascii=False)


@api_home.route('/home/ipCount', methods=['POST'])
def get_ipCount():
    client = MySQLClient("hdjd")
    rows_ipCount = client.query(f"""
    select count(ip)
from t_hdjd_log
where ip is not null
  and (url = 'http://www.laotianshi.top/screen' or url = 'http://www.laotianshi.top/screen/lv_monitor/' or url = 'http://www.laotianshi.top/screen/tie_monitor/' or url = 'http://www.laotianshi.top/screen/ngc_monitor/')
  and date_format(update_time, '%Y-%m-%d') = CURDATE()
    """, None)
    result = dict({
        "ipCount": 0,
        "ipDisCount": 0
    })
    if len(rows_ipCount) > 0:
        result["ipCount"] = rows_ipCount[0][0]

    rows_ipDisCount = client.query(f"""
    select count(distinct ip)
from t_hdjd_log
where ip is not null
  and (url = 'http://www.laotianshi.top/screen' or url = 'http://www.laotianshi.top/screen/lv_monitor/ ' or url = 'http://www.laotianshi.top/screen/tie_monitor/' or url = 'http://www.laotianshi.top/screen/ngc_monitor/' )
  and date_format(update_time, '%Y-%m-%d') = CURDATE()
    """, None)
    if len(rows_ipDisCount) > 0:
        result["ipDisCount"] = rows_ipDisCount[0][0]
    return json.dumps(result, ensure_ascii=False)
