from decimal import Context
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from course import views
from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from . models import *
# Create your views here.
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth import logout as django_logout

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views import View

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .utils import account_activation_token
from .filters import StudentDataFilter
from django.views.generic import ListView
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            email = email.lower()
            user = authenticate(request,email=email, password=password)

            if user is not None:
                auth_login(request,user)
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password")

        return render(request,'accounts/login.html')

def singup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            method_dict = request.POST.copy()
            first_name = method_dict.get('fullname')
            phone = method_dict.get('phone')
            emailaddress = method_dict.get('emailaddress')
            password = method_dict.get('password1')
            password2 = method_dict.get('password2')
            is_student = True
            email = emailaddress.lower()

            if password == password2:
                
                if User.objects.filter(email=email).exists():
                        messages.error(request, 'Email already taken!')
                else:
                    user =User.objects.create_user(first_name=first_name,phone=phone, email=email,password=password,is_student=is_student)
                    user.is_active = False
                    user.save()
                    # student = Student.objects.create(user=user,name=first_name)
                    uidb64= urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    domain = 'elearn.tunerpage.com'
                    link = reverse('activate', kwargs={'uidb64':uidb64,'token':token})
                    activate_url = 'https://'+domain+link
                    email_subject = 'Activate Your Account'

                    email_body = 'Hi '+user.first_name+"\nWelcome To Tunerpage Learning Platform.\nYou are almost done. To activate your account, please click the link below:\n \n"+activate_url+"\nIf you did not send the request, please ignore this email. Please do not reply to this email."+"\n \n \nBest Regards,\nTunerpage Team"+"\nFor any support, email us at: elearning.tunerpage@gmail.com"
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@tunerpage.com',
                        [emailaddress],
                    )
                    email.send(fail_silently=False)
                    messages.success(request, 'You are successfully registered! \n Please Chek your email to active your account')
                    return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request, 'Password does not match!')

            return HttpResponseRedirect(reverse('signup'))
    return render(request,'accounts/singup.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')



def instractorDetails(request,instractor_id):
    instractor = Instractor.objects.get(id=instractor_id)

    context={
        'instractor': instractor,
    }
    return render(request,'accounts/instractor_profile.html',context)

def allInstractor(request):
    instractor = Instractor.objects.all().prefetch_related('user')
    context={
        'instractor':instractor
    }
    return render(request,'accounts/all_instractor.html',context)


def registeredCourse(request):
    if request.user.is_authenticated:
        student = request.user
        course = Student.objects.filter(user =student,confirm=True).first()
        

        context ={
            'course':course
        }
        return render(request,'accounts/registered_course.html',context)
    else:
        return render(request,'accounts/registered_course.html')



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'elearn.tunerpage.com',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@elearn.tunerpage.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})




@user_passes_test(lambda u: u.is_superuser)
def studentData(request):
    students = Student.objects.all()
    paginator = Paginator(students,15)
    page = request.GET.get('page')
    student_pagination = paginator.get_page(page)
    context={
        'students':student_pagination
    }
    return render(request,'admin/student_data.html',context)

# @user_passes_test(lambda u: u.is_superuser)
# class studentData(ListView):
#     model = Student
#     tamplate_name = 'admin/data.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["filter"] = StudentDataFilter(self.request.GET,queryset=self.get_queryset())
#         return context
        