from django.urls import path
from app_user import views
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.conf.urls import include, url

app_name = 'user'

urlpatterns = [
    path('userRegistration', views.userRegistration.as_view(), name='userRegistration'),
    path('verify_otp', views.otp_vrfy, name='verify_otp'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout.as_view(), name='logout'),
    path('userVldt', views.userVldt, name='userVldt'),
    path('userFound', views.userFound, name='userFound'),
    path('emailCheck_db', views.emailCheck_db, name='emailCheck_db'),

    path('change/password/', login_required(views.change_password), name='change_password'),
]
