from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

from utils.db import MySQLClient


def my_task():
    sql_lv = f"""
    insert into t_hdjd_product_monitor_lv (changhao,
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
            qinglizaizhi)
    select changhao,
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
            qinglizaizhi from t_hdjd_product_monitor_lv where  DATE_FORMAT(update_time, '%Y-%m-%d') = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    """

    sql_tie = f"""
        insert into t_hdjd_product_monitor_tie (changhao,
       jinrizhixin,
       jinrihexiang,
       jinrikaixiang,
       benzhouhexiang,
       yueduzhixin,
       jinrizhuanxu,
       benzhouzhuanxu,
       yueduzhuanxu,
       yueduxiaoshou,
       maopichengpin,
       damo,
       rechuli,
       jingxiu,
       maopijianyan,
       tuzhuang,
       maopizaizhi,
       jinrijiagong,
       benzhoujiagong,
       yuedujiagong,
       jiagong_yueduxiaoshou,
       jiagongzaizhi,
       jinriqingli,
       benzhouqingli,
       yueduqingli,
       qinglizaizhi)
        select changhao,
       jinrizhixin,
       jinrihexiang,
       jinrikaixiang,
       benzhouhexiang,
       yueduzhixin,
       jinrizhuanxu,
       benzhouzhuanxu,
       yueduzhuanxu,
       yueduxiaoshou,
       maopichengpin,
       damo,
       rechuli,
       jingxiu,
       maopijianyan,
       tuzhuang,
       maopizaizhi,
       jinrijiagong,
       benzhoujiagong,
       yuedujiagong,
       jiagong_yueduxiaoshou,
       jiagongzaizhi,
       jinriqingli,
       benzhouqingli,
       yueduqingli,
       qinglizaizhi from t_hdjd_product_monitor_tie where  DATE_FORMAT(update_time, '%Y-%m-%d') = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        """

    sql_ngc = f"""
    insert into t_hdjd_product_monitor(changhao,zaoxingzhixin,hexiang,kaixiangqingli,damo,rechuli,jingxiu,maopijianyan,tuzhuang, jiagong,jiagongjianyan )
    select changhao,zaoxingzhixin,hexiang,kaixiangqingli,damo,rechuli,jingxiu,maopijianyan,tuzhuang, jiagong,jiagongjianyan from t_hdjd_product_monitor where  DATE_FORMAT(update_time, '%Y-%m-%d')=DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    """


    client = MySQLClient("hdjd")
    client.exec(sql_lv, None)
    client.exec(sql_ngc, None)
    client.exec(sql_tie, None)
    print("任务执行中...")



