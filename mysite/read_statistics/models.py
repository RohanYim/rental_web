from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


# Create your models here.

class ReadCount(models.Model):
    read_count = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # 用外键找到对应的模型
    object_id = models.PositiveIntegerField()  # 模型的主键
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面两条合成一个generic外键

class Counter():
    def get_read_count(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readcount = ReadCount.objects.get(content_type=ct, object_id=self.pk)
            return readcount.read_count
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_count = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # 用外键找到对应的模型
    object_id = models.PositiveIntegerField()  # 模型的主键
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面两条合成一个generic外键