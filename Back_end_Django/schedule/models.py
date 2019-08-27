import json

from django.db import models


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='姓名')

    class Meta:
        db_table = 'schedule_teacher'
        verbose_name = verbose_name_plural = '教师'

    def __repr__(self):
        return self.__repr__()

    def __str__(self):
        return self.name


class Major(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, verbose_name='课程名')
    duration = models.IntegerField(verbose_name='周期')
    order = models.IntegerField(unique=True, verbose_name='顺序')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')

    teachers = models.ManyToManyField(Teacher, related_name='majors', verbose_name='教师')

    class Meta:
        db_table = 'schedule_major'
        ordering = ('order',)
        verbose_name = verbose_name_plural = '课程'

    @property
    def info(self):
        return {
            'id': self.id,
            'majorTitle': self.title,
            'options': [teacher.name for teacher in self.teachers.all()],
            'duration': self.duration
        }

    def __repr__(self):
        return self.__repr__()

    def __str__(self):
        return self.title


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='班级名')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')

    majors = models.ManyToManyField(Major, through='Archive', related_name='classes')

    class Meta:
        db_table = 'schedule_class'
        ordering = ('name',)
        verbose_name = verbose_name_plural = '班级'

    @property
    def info(self):
        return {
            'id': self.id,
            'className': self.name,
        }

    def __repr__(self):
        return self.__repr__()

    def __str__(self):
        return self.name


class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Class, models.CASCADE)
    major_id = models.ForeignKey(Major, models.CASCADE)
    info = models.TextField()

    class Meta:
        db_table = 'schedule_archive'
        unique_together = (('class_id', 'major_id'),)

    @property
    def info_obj(self):
        return json.loads(self.info)

    @info_obj.setter
    def info_obj(self, value):
        self.info = json.dumps(value, ensure_ascii=False)

    def __repr__(self):
        return self.__repr__()

    def __str__(self):
        return self.info
