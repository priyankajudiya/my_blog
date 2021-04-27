from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    try:
        request.session['log_user'] = str(request.user)
    except:pass
    return render(request, 'app_core/home.html', {})