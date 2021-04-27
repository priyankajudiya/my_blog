"""project_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_user import views as resetView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('verification/', include('verify_email.urls')),
    path('', include('app_core.urls')),
    path('user/', include('app_user.urls')),
    path('post/', include('app_post.urls')),
    path('accounts/reset/done/', resetView.resetDone),
    path('accounts/password_change/', login_required(resetView.change_password)),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html')),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)