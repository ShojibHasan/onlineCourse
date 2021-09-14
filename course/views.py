from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse
from django.contrib import messages
from account.models import Instractor
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from account.utils import account_activation_token
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf  import csrf_exempt
# Create your views here.


# def cartItemsUpdates(request):
#     if request.user.is_authenticated:
#         student = request.user.student
#         order,created = Order.objects.get_or_create(student=student, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         items =[]
#         order = {'get_cart_totla':0, 'get_cart_items':0}
#         cartItems = order['get_cart_items']

#     context={
#         'cartItems':cartItems,
#     }

#     return HttpResponse(context)

def index(request):
    # course = Course.objects.all().order_by('created_at')
    course = Course.objects.select_related('category').order_by('created_at')
    category = Category.objects.all()
    instractor = Instractor.objects.all()
    if request.user.is_authenticated:
        student = request.user
        order,created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context ={
        'category':category,
        'instractor':instractor,
        'course':course,
        'cartItems':cartItems
        
    }
    return render(request,'includes/index.html',context)


def courses(request):
    if request.user.is_authenticated:
        student = request.user
        order,created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping': False}
        cartItems = order['get_cart_items']

    course = Course.objects.all()
    context ={
        
        'course':course,
        'cartItems':cartItems,
    }
    return render(request,'course/courses.html',context)



def courseDetails(request,course_id):

    course = Course.objects.all()
    if request.user.is_authenticated:
        student = request.user
        order,created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    course = Course.objects.get(id=course_id)
    
    context ={
        'items':items,
        'course':course,
        'cartItems':cartItems,
    }
    return render(request,'course/course_details.html',context)


@login_required
def cart(request):
    if request.user.is_authenticated:
        student = request.user
        order,created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping': False}
        cartItems = order['get_cart_items']        

    context ={
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request,'course/cart.html',context)



@login_required
def checkout(request):
    if request.user.is_authenticated:
        student = request.user
        order,created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0,'get_course_name': 0}
        cartItems = order['get_cart_items']  

    context ={
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request,'course/checkout.html',context)


@login_required
def updateItem(request):
    data = json.loads(request.body)
    courseId = data['courseId']
    action = data['action']



    student = request.user
    course = Course.objects.get(id=courseId)
    order,created = Order.objects.get_or_create(student=student, complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order,course=course)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse("Course Was Added", safe=False)


def enrollCourse(request):
    if request.user.is_authenticated:
        student_data = request.user
        if request.method == "POST" and request.FILES['image']:    
                course_enrolled = request.POST.get('course_enrolled')
                name = request.POST.get('name')
                email = request.POST.get('email')
                date_of_birth = request.POST.get('date_of_birth')
                education_qualification = request.POST.get('education_qualification')
                institution_name = request.POST.get('institution_name')
                image = request.FILES.get('image')
                student_address = request.POST.get('student_address')
                
                

                course_objects = Course.objects.get(name=course_enrolled)
                student_email = email
                if Student.objects.filter(email=email).exists():
                    messages.error(request, 'Error!! This Trx ID already used.')
                    return render(request,'course/error.html')
                else:
                    student = Student.objects.get_or_create(course_enrolled=course_objects,
                                    user=student_data,
                                    name =name,
                                    email=email,
                                    date_of_birth=date_of_birth,
                                    education_qualification=education_qualification,
                                    institution_name=institution_name,
                                    image=image,
                                    student_address=student_address,
                               )
                    # student.save()

                # Send email to Student
                    
                    email_subject = 'Registration Sucessfull'

                    email_body = 'Hi '+name+"\nThanks for choosing us. We will contact you as soon as possible"
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@onlinecourse.com',
                        [email],
                    )
                    email.send(fail_silently=False)

                    

                    if request.user.is_authenticated:
                        student = request.user
                        order,created = Order.objects.get_or_create(student=student, complete=False)
                        items = order.orderitem_set.all()
                        cartItems = order.get_cart_items
                    else:
                        items =[]
                        order = {'get_cart_total':0, 'get_cart_items':0,'get_course_name': 0}
                        cartItems = order['get_cart_items'] 
                        cartItems.delete()

                    total_student = Course.objects.get(name=course_objects)
                    total_student.total_student_enrolled +=1
                    total_student.save()
                    messages.success(request, 'Thanks for Enroll this Course')

                    return render(request,'course/confirm.html')
            
        else:
            return render(request,'course/error.html')





def termsAndConditions(request):
    return render(request,'includes/terms_and_conditions.html')

def privacyPolicy(request):
    return render(request,'includes/privacy_policy.html')


def ContactUs(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        obj= Contact(name=name,email=email,subject=subject,message=message)
        obj.save()
        messages.success(request,'Thanks for contacting us. We got your message.\nPlease check your email for updates ')
        return HttpResponseRedirect(reverse('contact_us'))
    return render(request,'includes/contact.html')

def allCourse(request):
    course = Course.objects.all().prefetch_related('category')
    context = {
        'course':course
    }
    return render(request,'course/all_course.html',context)

@login_required
def couponConfirmation(request):
    return render(request,'course/coupon_confirmation.html')

def CouponCart(request):
    if request.user.is_authenticated:
        student = request.user
        order,created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping': False}
        cartItems = order['get_cart_items']        

    context ={
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request,'course/coupon_cart.html',context)

@login_required
def CheckoutWithCoupon(request):
    if request.user.is_authenticated:
        student = request.user
        order,created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0,'get_course_name': 0}
        cartItems = order['get_cart_items']  

    context ={
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request,'course/checkout_with_coupon.html',context)


# @csrf_exempt
# def handlerequest(request):
#     ...
    


def error_404(request,exception):
    return render(request,'404.html')

def error_500(request):
    return render(request,'404.html')