
from django.conf.urls import handler500, url
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.site.site_header= "OnlineCourse Admin Panel"
admin.site.site_title = "Welcome To OnlineCourse Dashboard"
admin.site.index_title = "Welcome to OnlineCourse"
urlpatterns = [

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('admin/', admin.site.urls),
    path('accounts/',include('account.urls')),
    path('',include('course.urls')),
    path('summernote/', include('django_summernote.urls')),
]
if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns= urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'course.views.error_404'
handler500 = 'course.views.error_500'