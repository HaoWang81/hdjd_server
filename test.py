import pandas as pd

# 将序列日期数字转换为日期时间格式并消除时间部分
date = pd.to_datetime(45378, origin='1899-12-30', unit='D', errors='raise', infer_datetime_format=False, exact=True, cache=False, utc=None, format=None)

# 打印转换后的日期
print(date)