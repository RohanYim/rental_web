import datetime
# 当前时间与开始结束时间相比较
def compare_time(startTime, endTime):
    now = datetime.datetime.now()
    d_start = datetime.datetime.strptime (startTime, '%Y-%m-%d %H:%M')
    d_end = datetime.datetime.strptime (endTime, '%Y-%m-%d %H:%M')
    result = (d_start<=now) and (d_end>=now)
    listing = d_start<now
    # 返回true就是现在在进行中
    return result, listing

def compare_time_when_listing(startTime,listingstartTime, endTime,listingendTime):
    has_start = datetime.datetime.strptime (startTime, '%Y-%m-%d %H:%M')
    has_end = datetime.datetime.strptime (endTime, '%Y-%m-%d %H:%M')
    new_start = datetime.datetime.strptime (listingstartTime, '%Y-%m-%d %H:%M')
    new_end = datetime.datetime.strptime (listingendTime, '%Y-%m-%d %H:%M')
    # 不在其中返回true，允许添加
    result =  (has_end<=new_start) or (new_end<=has_start)
    return result

# 结束时间应大于开始时间
def list_time(startTime, endTime):
    d_start = datetime.datetime.strptime (startTime, '%Y-%m-%d %H:%M')
    d_end = datetime.datetime.strptime (endTime, '%Y-%m-%d %H:%M')
    result = (d_start<d_end)
    return result

