from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # 用外键找到对应的模型
    object_id = models.PositiveIntegerField()  # 模型的主键
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面两条合成一个generic外键

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # 排序
    class Meta:
        ordering = ['-comment_time']