from django.db import models

# Create your models here.
class Subject(models.Model):
    no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    intro = models.CharField(max_length=1000,default = '')
    is_hot = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'tb_subject'


class Teacher(models.Model):
    no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.BooleanField(default=True)
    birth = models.DateField()
    intro = models.CharField(max_length=1000,default='')
    photo = models.CharField(max_length=255,default='')
    good_count = models.IntegerField(db_column='gcount',default=0)
    bad_count = models.IntegerField(db_column='bcount',default=0)
    subject = models.ForeignKey(Subject, models.DO_NOTHING, db_column='sno')

    class Meta:
        managed = False
        db_table = 'tb_teacher'

class User(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    username = models.CharField(
        max_length=20, unique=True, verbose_name='用户名'
    )
    password = models.CharField(max_length=128, verbose_name='密码')
    tel = models.CharField(max_length=20, verbose_name='手机号')
    reg_date = models.DateTimeField(
        auto_now_add=True, verbose_name='注册时间'
    )
    last_visit = models.DateTimeField(
        null=True, verbose_name='最后登录时间'
    )

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
