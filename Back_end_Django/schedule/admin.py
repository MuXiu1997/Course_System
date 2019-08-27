from django.contrib import admin

from .models import Class, Major, Teacher


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_show')
    search_fields = ('name',)


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'order', 'is_show', 'info')
    filter_horizontal = ('teachers',)
    search_fields = ('title',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
