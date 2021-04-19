from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from app_user import forms
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
instance = ''
otp = 0


class userRegistration(View):
    def get(self, request):
        form = forms.userRegistrationForm
        return render(request, 'app_user/userreg.html', {'form': form})

    def post(self, request):
        form = forms.userRegistrationForm(request.POST)
        if form.is_valid():
            global instance, otp
            instance = form.save(commit=False)
            instance.set_password(request.POST.get('password'))
            otp = random.randint(1111, 9999)
            # Below Code is for Sending otp mail
            to_mail = request.POST.get('email')
            subject = 'welcome to Blog World'
            message = f'Hi {instance.username}, thank you for registering in My Blog. Your OTP is: {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [to_mail, ]
            send_mail(subject, message, email_from, recipient_list)

            return render(request, 'app_user/otpverify.html')
        else:
            return HttpResponse('somthing wrong')

# OTP


def otp_vrfy(request):
    if request.method == 'POST':
        user_otp = int(request.POST.get('entered_otp'))
        # print(type(otp), type(user_otp))

        if user_otp == otp:
            to_mail = instance.email
            subject = 'welcome to My BLOG'
            message = f'Hi {instance.username}, Welcome to Blog. Your account is created'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [to_mail, ]
            send_mail(subject, message, email_from, recipient_list)
            instance.save()
            return redirect('user:login')
        else:
            return render(request, 'app_user/otpverify.html')
    else:
        return redirect('user:login')


# ajax user validate


def userVldt(request):
    usr = request.GET.get('username')

    try:
        user = User.objects.get(username=usr)
        print('Not availeble')
        return HttpResponse('Not availeble')
    except:
        print('Availeble')
        return HttpResponse('Availeble')
