from loguru import logger

from utils.db import MySQLClient


def my_task():
    logger.info('执行数据同步任务')
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
    insert into t_hdjd_product_monitor(changhao,zaoxingzhixin,hexiang,maopichengping,kaixiangqingli,qingli,damo,rechuli,jingxiu,caizhijianyan,maopijianyan,qinglibaozhuang,tuzhuang,tuzhuangjianyan,zhongjian, jiagong,jiagongqingli,jiagongjianyan,count_flag )
    select changhao,zaoxingzhixin,hexiang,maopichengping,kaixiangqingli,qingli,damo,rechuli,jingxiu,caizhijianyan,maopijianyan,qinglibaozhuang,tuzhuang,tuzhuangjianyan,zhongjian, jiagong,jiagongqingli,jiagongjianyan,count_flag  from t_hdjd_product_monitor where  DATE_FORMAT(update_time, '%Y-%m-%d')=DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    """

    sql_ngcInner = f"""
        insert into t_hdjd_product_monitor_ngc(
        changhao,
       zx_dmjz,
       zx_jrkx,
       zx_jrqs,
       zx_bzzx,
       zx_ydzx,
       dm_jrdm,
       dm_jrrcl,
       dm_jrjx,
       dm_jrndtjy,
       dm_bzdm,
       dm_yddm,
       dm_mpzz,
       yq_jryq,
       yq_jryqjy,
       yq_bzyq,
       yq_ydyq,
       jg_jrjg,
       jg_jrjgjy,
       jg_bzjg,
       jg_ydjg,
       jg_jgdw,
       jg_jgzz,
       mp_mpzjg,
       mp_bzmpzjg,
       mp_ydmpzjg,
       mp_cpk
        )
        select 
          changhao,
       zx_dmjz,
       zx_jrkx,
       zx_jrqs,
       zx_bzzx,
       zx_ydzx,
       dm_jrdm,
       dm_jrrcl,
       dm_jrjx,
       dm_jrndtjy,
       dm_bzdm,
       dm_yddm,
       dm_mpzz,
       yq_jryq,
       yq_jryqjy,
       yq_bzyq,
       yq_ydyq,
       jg_jrjg,
       jg_jrjgjy,
       jg_bzjg,
       jg_ydjg,
       jg_jgdw,
       jg_jgzz,
       mp_mpzjg,
       mp_bzmpzjg,
       mp_ydmpzjg,
       mp_cpk
          from t_hdjd_product_monitor_ngc where  DATE_FORMAT(update_time, '%Y-%m-%d')=DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        """

    client = MySQLClient("hdjd")
    client.exec(sql_lv, None)
    client.exec(sql_ngc, None)
    client.exec(sql_tie, None)
    client.exec(sql_ngcInner, None)
    logger.info('数据同步任务结束')
