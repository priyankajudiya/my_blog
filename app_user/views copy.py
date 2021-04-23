from django.contrib.auth.models import User
from app_user import forms
from django.conf import settings
from django.core.mail import send_mail
import random
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib import messages


# Create your views here.


##############################################  User Registration View
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

            request.session['log_user'] = request.POST.get('username')
            request.session['log_pass'] = request.POST.get('password')

            return render(request, 'app_user/otpverify.html')
        else:
            return HttpResponse('somthing wrong')

##############################################  OTP View
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


##############################################  ajax user validate
def userVldt(request):
    usr = request.GET.get('username')

    try:
        user = User.objects.get(username=usr)
        print('Not availeble')
        return HttpResponse('Not availeble')
    except:
        print('Availeble')
        return HttpResponse('Availeble')

##############################################  Login View
def userLogin(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            request.session['log_user'] = username

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            messages.add_message(request, messages.SUCCESS, 'Logged in successfully')
            return redirect('index')
        return HttpResponse('Log-in not successful')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            try:
                username = request.session['log_user']
                password = request.session['log_pass']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    request.session['log_user'] = username
                    messages.add_message(request, messages.SUCCESS, 'Registration in successfully')
                    del request.session['log_pass']
                    return redirect('index')
            except:pass
                
            return render(request, 'app_user/userlogin.html', {})

############################################## Log Out
class userLogout(View):
    def get(self, request):
        if request.user.is_authenticated:
            del request.session['log_user']
            logout(request)
            messages.add_message(request, messages.DANGER, 'Logged out successfully')
            return redirect('index')
        else:
            return redirect('user:login')


############################################# Username Ajax
from django.contrib.auth.models import User
def userFound(request):
    username = request.GET.get('username')
    try:
        User.objects.get(username=username)
        return HttpResponse('Username found')
    except:
        return HttpResponse('Username not found')