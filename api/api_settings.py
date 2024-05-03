import logging

from flask import Blueprint, request, jsonify
import pandas as pd

from utils.db import MySQLClient

api_settings = Blueprint('api_settings', __name__)


@api_settings.route('/settings/upload', methods=['POST'])
def settings_upload():
    type = request.args.get('type')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    pd.set_option('display.max_columns', None)

    client = MySQLClient('hdjd')
    try:
        if type == '2':  # 工段明细
            df = pd.read_excel(file, sheet_name="毛坯生产数量1")
            df.fillna(0, inplace=True)
            data = []
            for index, row in df.iterrows():
                production_date = None
                try:
                    date = pd.to_datetime(row[0], origin='1899-12-30', unit='D', errors='raise',
                                          infer_datetime_format=False,
                                          exact=True, cache=False, utc=None, format=None)
                    production_date = str(date)
                except Exception as e:
                    logging.error(f'非日期格式,{e}')
                data.append((row[1], row[2], row[3], row[5], row[9], production_date))
            insert_sql = "insert into t_hdjd_blank_production(production_name,check_num,per_weight,production_company,production_unit,production_date) values(%s,%s,%s,%s,%s,%s) "
            client.delete("delete from t_hdjd_blank_production ", None)
            client.insert_batch(insert_sql, data)
        elif type == '1':  # 生产监控
            df = pd.read_excel(file, sheet_name="3.21日生产监控")
            df.fillna(0, inplace=True)
            data = []
            for index, row in df.iterrows():
                if (index + 1) >= 3 and str(row[33]) != 'nan' and str(row[33]) != '?':
                    data.append(
                        (row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42],
                         row[43], row[44], row[45], row[46], row[47], row[48], row[49], row[50],
                         (1 if row[51] == 1 else 0)))
            sql = (
                "insert into t_hdjd_product_monitor(changhao,zaoxingzhixin,hexiang,maopichengping,kaixiangqingli,qingli,damo,rechuli,jingxiu,caizhijianyan,maopijianyan,qinglibaozhuang,tuzhuang,tuzhuangjianyan,zhongjian,jiagong,jiagongqingli,jiagongjianyan,count_flag) "
                "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            client.delete("delete  from t_hdjd_product_monitor where DATE_FORMAT(update_time, '%Y-%m-%d')=CURDATE() ",
                          None)
            client.insert_batch(sql, data)
        elif type == '3':
            df = pd.read_excel(file, sheet_name="铝件生产监控")
            df.fillna(0, inplace=True)
            data = []
            for index, row in df.iterrows():
                if (index + 1) >= 2 and str(row[0]) != 'nan' and str(row[0]) != '?':
                    data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                 row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18],
                                 row[19]))

            sql = ("""
            insert into t_hdjd_product_monitor_lv ( changhao,
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
            qinglizaizhi
            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """)
            client.delete(
                "delete  from t_hdjd_product_monitor_lv where DATE_FORMAT(update_time, '%Y-%m-%d')=CURDATE() ", None)
            client.insert_batch(sql, data)
        elif type == '4':
            df = pd.read_excel(file, sheet_name="铁件生产监控")
            df.fillna(0, inplace=True)
            data = []
            for index, row in df.iterrows():
                if (index + 1) >= 2 and str(row[0]) != 'nan' and str(row[0]) != '?':
                    data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                 row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18],
                                 row[19], row[20], row[21], row[22], row[23], row[24], row[25]))

            sql = ("""
                   insert into t_hdjd_product_monitor_tie ( changhao,
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
       qinglizaizhi) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   """)
            client.delete(
                "delete  from t_hdjd_product_monitor_tie where DATE_FORMAT(update_time, '%Y-%m-%d')=CURDATE() ", None)
            client.insert_batch(sql, data)
        elif type == '5':  # ngc内部监控
            df = pd.read_excel(file, sheet_name="南高齿监控表")
            df.fillna(0, inplace=True)
            data = []
            for index, row in df.iterrows():
                if (index + 1) >= 3 and str(row[0]) != 'nan' and str(row[0]) != '?':
                    data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                 row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18],
                                 row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[25]))
            sql = ("""
                               insert into t_hdjd_product_monitor_ngc ( 
                               
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
                               ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                               """)
            client.delete(
                "delete  from t_hdjd_product_monitor_ngc where DATE_FORMAT(update_time, '%Y-%m-%d')=CURDATE() ", None)
            client.insert_batch(sql, data)
        return f'成功'
    except Exception as e:
        return f'异常：{e}'
