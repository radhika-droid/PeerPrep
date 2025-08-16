from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core.views import (
    index, contact_success, register, dashboard,
    home, feature, about, contact,forgot_password
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('feature/', feature, name='feature'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('contact-success/', contact_success, name='contact_success'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('forgot-password/', forgot_password, name='forgot_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
