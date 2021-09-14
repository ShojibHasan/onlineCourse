from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class CourseAdmin(SummernoteModelAdmin):
    summernote_fields = ('course_description','what_you_will_learn','course_requirements')



class BatchNumberAdmin(admin.ModelAdmin):
    class Meta:
        model = Student
    list_display = ['id','name','course']
    list_display_links = ['id','name','course']
    search_fields = ('name'),
    list_per_page = 20


class CourseVideoAdmin(admin.StackedInline):
    model = CourseVideo
 
@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    inlines = [CourseVideoAdmin]
 
    class Meta:
       model = CourseContent
 
@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category)
admin.site.register(BatchNumber,BatchNumberAdmin)
admin.site.register(Coupon)
admin.site.register(Course,CourseAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact )