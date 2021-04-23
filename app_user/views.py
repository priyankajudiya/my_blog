from django.contrib.auth.models import User
from app_user import forms
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib import messages
from verify_email.email_handler import send_verification_email

# Create your views here.


##############################################  User Registration View
class userRegistration(View):
    def get(self, request):
        form = forms.userRegistrationForm
        return render(request, 'app_user/userreg.html', {'form': form})

    def post(self, request):
        form = forms.userRegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(request.POST.get('password'))
            send_verification_email(request, form)
            request.session['log_user'] = request.POST.get('username')
            request.session['log_pass'] = request.POST.get('password')
            return render(request, 'app_user/otpverify.html')
        else:
            return HttpResponse('somthing wrong')

##############################################  OTP View
def otp_vrfy(request):
    if request.method == 'POST':
        return render(request, 'app_user/otpverify.html')
    else:
        return redirect('user:login')


##############################################  ajax user validate
def userVldt(request):
    usr = request.GET.get('username')
    try:
        User.objects.get(username=usr)
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
            messages.add_message(request, messages.SUCCESS, 'Logged in successfully')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
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
                    messages.add_message(request, messages.SUCCESS, 'Email Verified successfully')
                    del request.session['log_pass']
                    return redirect('index')
            except:
                pass
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
def userFound(request):
    username = request.GET.get('username')
    try:
        User.objects.get(username=username)
        return HttpResponse('Username found')
    except:
        return HttpResponse('Username not found')