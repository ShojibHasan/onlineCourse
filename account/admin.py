from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class InstractorAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')

class StudentAdmin(admin.ModelAdmin):
    class Meta:
        model = Student
    list_display = ['id','name','email','course_enrolled','batch_number','confirm']
    list_display_links = ['id','name','email','course_enrolled']
    list_filter =('email'),
    list_editable = ('confirm'),
    search_fields = ('name','email','phone','course_enrolled'),
    list_per_page = 20


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model: User
    list_display = ['id','email','phone','first_name','is_student']
    list_display_links = ['id','email','phone','first_name']
    # list_filter =('first_name','phone'),
    list_editable = ('is_student'),
    search_fields = ('first_name','email','phone'),
    list_per_page = 20


admin.site.register(Student,StudentAdmin)
admin.site.register(Instractor,InstractorAdmin)
admin.site.register(User,UserAdmin)