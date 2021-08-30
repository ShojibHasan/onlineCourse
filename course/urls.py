from django.urls import path
from . import views



urlpatterns = [
    path('',views.index,name="index"),
    path('courses/',views.courses,name="courses"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('course/<int:course_id>/', views.courseDetails,name='course_details'),
    path('update_course/',views.updateItem,name="update_course"),
    path('enroll/',views.enrollCourse,name="enroll"),
    path('terms_of_use/',views.termsAndConditions,name="terms_of_use"),
    path('privacy_policy/',views.privacyPolicy,name="privacy_policy"),
    path('contact_us/',views.ContactUs,name="contact_us"),
    path('all_course/',views.allCourse,name="all_course"),

    path('confirmation/',views.couponConfirmation,name='coupn_confirmation'),
    path('coupon_cart/',views.CouponCart,name='coupon_cart'),
    path('checkout_with_coupon/',views.CheckoutWithCoupon,name='checkout_with_coupon'),
   

    # path('handlerequest',views.handlerequest,name='handlerequest')
]
