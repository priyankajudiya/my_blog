from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout

def userLogin(request):
    user = authenticate()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            request.session['log_user'] = username

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            if user.username == 'admin':
                return redirect('../admin/')
            else:
                return redirect('index')
        return HttpResponse('Log-in not successful')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'app_user/userlogin.html', {})

############################################## Log Out
def userLogout(request):
    try:
        del request.session['log_user']
        logout(request)
    except:
        logout(request)
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