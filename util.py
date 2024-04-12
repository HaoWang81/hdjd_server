# -*- coding: utf-8 -*-
import json

import pandas as pd


# 合箱欠数
# 35
# 打磨欠数
# 39
# 精修欠数
# 41
# 毛坯检验欠数
# 43
# 涂装欠数
# 45
# 涂装检验欠数
# 46
# 加工欠数
# 48
# 加工检验欠数
# 50


def readExcle(excle_file):
    pd.set_option('display.max_columns', None)

    df = pd.read_excel(excle_file, sheet_name='生产监控')
    result = []
    for index, row in df.iterrows():
        if (index + 1) >= 3:
            if str(row[0]) != 'nan' and str(row[0]) != '?':
                t1 = row[35]
                t2 = row[39]
                t3 = row[41]
                t4 = row[43]
                t5 = row[45]
                t6 = row[46]
                t7 = row[48]
                t8 = row[50]
                if True:
                    result.append(
                        (row[34],
                         t1,
                         t2,
                         t3,
                         t4,
                         t5,
                         t6,
                         t7,
                         t8))
    return result


def readExcleByScreen(excle_file):
    pd.set_option('display.max_columns', None)

    # file_path = excle_file.save("./" + excle_file.filename)
    df = pd.read_excel(excle_file, sheet_name='3.21日生产监控')
    result = []
    for index, row in df.iterrows():
        if (index + 1) >= 3:
            if str(row[0]) != 'nan' and str(row[0]) != '?':
                t1 = row[34]
                t2 = row[35]
                t3 = row[37]
                t4 = row[39]
                t5 = row[40]
                t6 = row[41]
                t7 = row[43]
                t8 = row[45]
                t9 = row[48]
                t10 = row[50]
                if t1==0 and   t2==0 and  t3==0 and  t4==0 and  t5==0 and  t6==0 and  t7==0 and  t8==0 and  t9==0 and   t10==0 :
                    continue
                else:
                    result.append(
                        (row[33],
                         t1,
                         t2,
                         t3,
                         t4,
                         t5,
                         t6,
                         t7,
                         t8, t9, t10))
    array_with_lists = [list(t) for t in result]

    # 转换为JSON格式
    json_data = json.dumps(array_with_lists, ensure_ascii=False)

    return json.loads(json_data)


import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from PIL import Image
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot as driver


def buildHtml(result):
    合箱欠数 = 0
    打磨欠数 = 0
    精修欠数 = 0
    毛坯检验欠数 = 0
    涂装欠数 = 0
    涂装检验欠数 = 0
    加工欠数 = 0
    加工检验欠数 = 0

    # 创建柱状图
    bar = (
        Bar()
        .add_xaxis(["合箱欠数", "打磨欠数", "精修欠数", "毛坯检验欠数", "涂装欠数", "涂装检验欠数", "加工欠数",
                    "加工检验欠数"])
        .add_yaxis("欠数统计",
                   [abs(合箱欠数), abs(打磨欠数), abs(精修欠数), abs(毛坯检验欠数), abs(涂装欠数), abs(涂装检验欠数),
                    abs(加工欠数), abs(加工检验欠数)])
        .set_global_opts(title_opts=opts.TitleOpts(title="各工段欠数情况统计"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}))
    )

    # 生成 HTML 文件
    html_path = "chart.html"
    bar.render(html_path)

    # 生成图像
    make_snapshot(driver, bar.render(), "chart.png")

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = '773872428@qq.com'
    msg['To'] = '773872428@qq.com'
    # msg['To'] = '773872428@qq.com'
    msg['Subject'] = '工段欠数汇总'

    desc = ""
    names = ["合箱欠数", "打磨欠数", "精修欠数", "毛坯检验欠数", "涂装欠数", "涂装检验欠数", "加工欠数", "加工检验欠数"]
    values = [abs(合箱欠数), abs(打磨欠数), abs(精修欠数), abs(毛坯检验欠数), abs(涂装欠数), abs(涂装检验欠数),
              abs(加工欠数), abs(加工检验欠数)]
    for index, item in enumerate(names):
        desc += f"<span style=\"line-height: 50px;\"> {index + 1}、{item}：<b style=\"font-size: 22px;\">{values[index]}</b>&nbsp;件</span><br>"
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y年%m月%d日")

    detail = ""
    for index, item in enumerate(result):
        detail += " <tr style=\"display: table;width: 100%;table-layout: fixed;\">"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{index + 1}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[0]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[1]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[2]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[3]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[4]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[5]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[6]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[7]}</td>"
        detail += f"<td style=\"  border: 1px solid #dddddd; text-align: left; padding: 8px;\">{item[8]}</td>"
    detail += "</tr> "

    # 添加 HTML 正文
    html_content = (f"""
    <html>
<meta charset="UTF-8">
<body>
<h3>姚中霞，您好</h3>
<span>截止至 {formatted_date} ，所涉及工段欠数信息如下：</span>
<div style="display: flex;margin-top: 30px;margin-left: 30px;">
    <div class="desc">
{desc}
    </div>
    <div style="margin-left: 150px">
        <img src="cid:chart">
    </div>
</div>
<a href=>
<table style="border-collapse: collapse;margin-left:25px;width:75%">
    <thead style="width:98.5%;display: table;table-layout: fixed;">
    <tr style="display: table;width: 100%;table-layout: fixed;">
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">序号</th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">厂号</th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">合箱欠数</th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">打磨欠数</th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">精修欠数</th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">
            毛坯检验欠数
        </th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">涂装欠数</th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">
            涂装检验欠数
        </th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">加工欠数</th>
        <th style="  border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f2f2;">
            加工检验欠数
        </th>
    </tr>
    </thead>
    <tbody style=" display: block;height: 200px;overflow-y: auto;">
    {detail}
    </tbody>
</table>
</body>

</html>
    """)
    msg.attach(MIMEText(html_content, 'html'))

    # 缩小图像
    def resize_image(image_path, max_width, max_height):
        img = Image.open(image_path)
        img.thumbnail((max_width, max_height))
        return img

    # 等比例缩放图像

    # 调整大小
    resized_img = resize_image("chart.png", 800, 500)

    resized_img.save("chart_resized.png", quality=10)

    # 添加图像
    with open("chart_resized.png", "rb") as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<chart>')
        msg.attach(img)

    # 通过 SMTP 发送邮件
    smtp_server = 'smtp.qq.com'
    smtp_port = 465
    smtp_username = '773872428@qq.com'
    smtp_password = 'goqselhckzydbfbe'

    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(smtp_username, smtp_password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    os.remove('chart.html')
    os.remove('chart.png')
    os.remove('chart_resized.png')
