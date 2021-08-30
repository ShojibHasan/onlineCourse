from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

from django.views.decorators.cache import cache_page


urlpatterns = [
    path('login/',views.login,name='login'),
    path('singup/',views.singup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(),name='activate'),

    #password Reset 
    
    # path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/forgot_password.html"), name="reset_password"),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password_sent.html"),name ="password_reset_done"),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name ="password_reset_complete"),

    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),      


    #instructor

    path('instructor/<int:instractor_id>/',views.instractorDetails,name='instractors_details'),
    path('instructors/',views.allInstractor,name='all_instructors'),
    path('enrolled_course/',views.registeredCourse,name='enrolled_course'),
    path('student_data/',views.studentData,name='student_data'),
    # path('data/', views.studentData.as_view(),name="data"),
]
