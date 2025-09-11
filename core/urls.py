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

     path('faq/', views.faq_view, name='faq'),
       path('faq/add/', views.add_faq, name='add_faq'),
          path('faq/delete/<int:faq_id>/', views.delete_faq, name='delete_faq'),
    # Progress Tracking URLs
    path('progress/', views.progress_tracking, name='progress_tracking'),
    path('api/progress-dashboard/', views.get_progress_dashboard_data, name='api_progress_dashboard'),
    path('api/goals/', views.get_goals, name='api_goals'),
    path('api/create-goal/', views.create_goal, name='api_create_goal'),
    path('api/goal/<int:goal_id>/', views.get_goal_detail, name='api_goal_detail'),
    path('api/update-goal-progress/<int:goal_id>/', views.update_goal_progress, name='api_update_goal_progress'),
    path('api/delete-goal/<int:goal_id>/', views.delete_goal, name='api_delete_goal'),
    path('api/log-study-session/', views.log_study_session, name='api_log_study_session'),
    path('api/set-weekly-goals/', views.set_weekly_goal, name='api_set_weekly_goals'),
    path('api/create-milestone/<int:goal_id>/', views.create_milestone, name='api_create_milestone'),
    path('api/toggle-milestone/<int:milestone_id>/', views.toggle_milestone, name='api_toggle_milestone'),
    path('api/recent-activity/', views.get_recent_activity, name='api_recent_activity'),
    # Add these URLs to your core/urls.py file (in the urlpatterns list)

    # Study Partners URLs
    path('find-study-partners/', views.find_study_partners, name='find_study_partners'),
    path('study-profile/', views.study_profile, name='study_profile'),
    path('api/search-study-partners/', views.search_study_partners, name='api_search_study_partners'),
    path('api/send-partner-request/', views.send_partner_request, name='api_send_partner_request'),
    path('my-partner-requests/', views.my_partner_requests, name='my_partner_requests'),
    path('api/respond-to-request/<int:request_id>/', views.respond_to_request, name='api_respond_to_request'),
    path('my-study-partners/', views.my_study_partners, name='my_study_partners'),
    path('api/schedule-session/', views.schedule_session, name='api_schedule_session'),
    path('api/partnership-sessions/<int:partnership_id>/', views.get_partnership_sessions, name='api_partnership_sessions'),
    path('api/complete-session/<int:session_id>/', views.complete_session, name='api_complete_session'),
    path('api/end-partnership/<int:partnership_id>/', views.end_partnership, name='api_end_partnership'),
]