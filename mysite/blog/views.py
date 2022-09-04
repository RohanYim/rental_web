from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from read_statistics.utils import read_statistics_once_read
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment

# Create your views here. 就是写都有哪些页面显示出来
# 模板
def blog_temp(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.BLOG_EACH_PAGE) # 每一页有多少个数据
    page_number = request.GET.get('page', 1)  # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_number)
    current_page = page_of_blogs.number  # 获取当前页码
    # page_range = [current_page - 2, current_page - 1, current_page,  current_page+ 1, current_page+ 2]
    if current_page > paginator.num_pages - 5:
        page_range = range(paginator.num_pages - 4,paginator.num_pages + 1)
    else:
        page_range = range(current_page, current_page + 5)
    

    context = {
        'page_of_blogs': page_of_blogs,   # 博客列表
        'blogs': page_of_blogs.object_list,  # 当前页的博客
        'page_range': page_range,   # 页码栏的构成
        'blog_types' : BlogType.objects.all(),  # 所有按博客分类后的博客
        'blog_dates' : Blog.objects.dates('create_time','month',order='ASC')  # 返回博客的创建时间，具体到月
    }
    return context
# 博客列表
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = blog_temp(request, blogs_all_list)
    return render(request, 'blog_list.html', context)
# 博客类型
def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = blog_temp(request, blogs_all_list)
    context['blog_type'] = blog_type  # 博客分类列表

    return render(request, 'blogs_with_type.html', context)
# 博客按照年月分类
def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = blog_temp(request, blogs_all_list)
    context['blog_dates'] = Blog.objects.dates('create_time','month',order='ASC')  # 返回博客的创建时间，具体到月
    context['blogs_with_date'] = '%s.%s' %(year,month)

    return render(request, 'blogs_with_date.html', context)
# 每一个博客的具体内容
def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookies = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)
    context = {
        'blog': blog,
        'previous_blog': Blog.objects.filter(create_time__gt=blog.create_time).last(), # 获取创建日期大于当前博客的所有博客,选取其中的最后一条
        'next_blog': Blog.objects.filter(create_time__lt=blog.create_time).first(),
        'comments': comments,
    }
    response = render(request, 'blog_detail.html', context)   # 响应
    response.set_cookie(read_cookies, 'true')    # 设置cookies，key，value，max_age(秒为单位)，expires（到哪天结束），若不加过期时间则在关闭浏览器时清除cookies
    return response
