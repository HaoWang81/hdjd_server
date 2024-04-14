from  datetime import datetime,timedelta


def getCurrentWeekNum(date):
    # 将日期转换为 datetime 对象
    date_obj = datetime.date.today()
    # 使用 isocalendar 方法获取 ISO 标准的年份和周数
    year, week_number, _ = date_obj.isocalendar()
    return week_number

def currentDateYYYYMMDD() -> str:
    yesterday = datetime.now() - timedelta(days=4)
    # 格式化为 %Y-%m-%d
    return yesterday.strftime("%Y-%m-%d")


if __name__ == '__main__':
    print(currentDateYYYYMMDD())


