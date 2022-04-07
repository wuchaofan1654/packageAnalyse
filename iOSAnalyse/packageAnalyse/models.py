from django.db import models

# Create your models here.


class Publish(models.Model):
    version = models.CharField(default='', max_length=50)
    build_no = models.CharField(default='', max_length=50)
    branch = models.CharField(default='', max_length=255)
    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = '版本发布记录表'
        verbose_name_plural = '版本发布记录表'
        ordering = ['-id']

    def __str__(self):
        return f'{self.version}-{self.build_no}【{self.branch}】'


class Module(models.Model):
    publish = models.ManyToManyField(to='Publish', default=0)
    module_name = models.CharField(default='', max_length=50)
    module_size = models.IntegerField(default=0)
    module_type = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = '模块大小记录表'
        verbose_name_plural = '模块大小记录表'
        ordering = ['-id']

    def __str__(self):
        return self.module_name

