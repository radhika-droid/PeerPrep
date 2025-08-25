from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main pages
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('feature/', views.feature, name='feature'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Auth pages
    path('contact-success/', views.contact_success, name='contact_success'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    
    # Success Stories
    path('success-stories/', views.success_stories, name='success_stories'),
    path('auth-check/', views.auth_check, name='auth_check'),
    path('get-success-stories/', views.get_success_stories, name='get_success_stories'),
    path('api/success-stories/', views.get_success_stories, name='api_success_stories'),
    path('add-success-story/', views.add_success_story, name='add_success_story'),
    path('react-to-story/<int:story_id>/', views.react_to_story, name='react_to_story'),
    path('user-reactions/<int:story_id>/', views.get_user_reactions, name='get_user_reactions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])