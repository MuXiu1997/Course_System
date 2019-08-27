from django.contrib import admin

from .models import Class, Major, Teacher


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_show')
    search_fields = ('name',)
    ordering = ('name',)


def teachers(major):
    return [teacher for teacher in major.teachers.all()]


teachers.__name__ = '教师'


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'order', 'is_show', teachers)
    filter_horizontal = ('teachers',)

    search_fields = ('title',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
