from django.shortcuts import render, get_object_or_404,redirect
from read_statistics.utils import get_week_read_date
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from django.contrib import auth
import datetime
from django.urls import reverse
from django.contrib.auth.models import User

def get_past_week_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = Blog.objects \
                    .filter(read_details__date__lte=today, read_details__date__gt=date) \
                    .values('id','title') \
                    .annotate(read_count_sum=Sum('read_details__read_count')) \
                    .order_by('-read_count_sum')   # 按照id，title groupby，分组求和，最后排序
    return read_details[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    week, read_nums = get_week_read_date(blog_content_type)

    # 使用缓存读取数据（缓存保存3600秒）
    hot_blogs_for_past_week = cache.get('hot_blogs_for_past_week')
    if hot_blogs_for_past_week is None:
        hot_blogs_for_past_week = get_past_week_hot_blog()
        cache.set('hot_blogs_for_past_week',hot_blogs_for_past_week, 3600)
    

    context = {
        'week': week,
        'read_nums' : read_nums,
        'hot_blogs_for_past_week': get_past_week_hot_blog(),
    }
    return render(request, 'home.html', context)

