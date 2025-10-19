from django.urls import path, include
from . import views

urlpatterns = [
    # Include app-specific URLs first
    path("notes/", include("notes.urls")),
    path("", include("peerprep.urls")),
   
    # Main app routes
    path('', views.index, name='index'),
    path('api/toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('success/', views.contact_success, name='contact_success'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    path('feature/', views.feature, name='feature'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("timetable/", views.timetable, name="timetable"),
    path('profile/', views.profile_view, name='profile'),


    # Success Stories URLs
    path('success-stories/', views.success_stories, name='success_stories'),
    path('add-success-story/', views.add_success_story, name='add_success_story'),
    path('react-to-story/<int:story_id>/', views.react_to_story, name='react_to_story'),
    path('user-reactions/<int:story_id>/', views.get_user_reactions, name='get_user_reactions'),

    # API Endpoints
    path('api/success-stories/', views.get_success_stories, name='api_success_stories'),
    path('api/auth-check/', views.auth_check, name='auth_check'),
]
