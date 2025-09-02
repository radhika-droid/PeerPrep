from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.contact_success, name='contact_success'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    path('feature/', views.feature, name='feature'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("timetable/", views.timetable, name="timetable"),

    # Success Stories URLs
    path('success-stories/', views.success_stories, name='success_stories'),
    path('add-success-story/', views.add_success_story, name='add_success_story'),
    path('react-to-story/<int:story_id>/', views.react_to_story, name='react_to_story'),
    path('user-reactions/<int:story_id>/', views.get_user_reactions, name='get_user_reactions'),
    path('api/success-stories/', views.get_success_stories, name='api_success_stories'),
    path('api/auth-check/', views.auth_check, name='auth_check'),
    
    # Questions & Answers URLs - NEW
    path('questions/', views.questions, name='questions'),
    path('api/questions/', views.get_questions, name='api_questions'),
    path('api/ask-question/', views.ask_question, name='api_ask_question'),
    path('api/question/<int:question_id>/', views.get_question_detail, name='api_question_detail'),
    path('api/answer-question/<int:question_id>/', views.answer_question, name='api_answer_question'),
    path('api/upvote-question/<int:question_id>/', views.upvote_question, name='api_upvote_question'),
    path('api/upvote-answer/<int:answer_id>/', views.upvote_answer, name='api_upvote_answer'),
    path('api/accept-answer/<int:answer_id>/', views.accept_answer, name='api_accept_answer'),
]