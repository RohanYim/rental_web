from django.contrib.contenttypes.models import ContentType
from .models import ReadCount, ReadDetail
from django.utils import timezone
from django.db.models import Sum
import datetime

# 如果没有读到cookies，访问量就不增加
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # 检查是否存在readcount记录
        readcount, created = ReadCount.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 总阅读计数加一    
        readcount.read_count += 1
        readcount.save()

        date = timezone.now().date()
        readcount_today, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        # 当天阅读数量加一
        readcount_today.read_count += 1
        readcount_today.save()
    return key

def get_week_read_date(content_type):
    today = timezone.now().date()
    week = []
    week_count = []
    # 从今天开始前七天的阅读数量
    for i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)  # 日期差量，得到昨天
        week.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_count_sum=Sum('read_count'))
        week_count.append(result['read_count_sum'] or 0)
    return week, week_count

# def get_past_week_hot_blog(content_type):
#     today = timezone.now().date()
#     date = today - datetime.timedelta(days=7)
#     read_details = ReadDetail.objects \
#                     .filter(content_type=content_type, date__lt=today, date__gte=date) \
#                     .values('content_type','object_id') \
#                     .annotate(read_count_sum=Sum('read_count')) \
#                     .order_by('-read_count_sum')
#     return read_details[:7]