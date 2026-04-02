from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main pages
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("feature/", views.feature, name="feature"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact-success/", views.contact_success, name="contact_success"),

    # Authentication
    path("register/", views.register, name="register"),
    path("registration/", views.register, name="registration"),  # Required by index.html
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("logged-out/", views.logged_out, name="logged_out"),     # Required by index.html
    path("forgot-password/", views.forgot_password, name="forgot_password"),

    # User profile + dashboard
    path("profile/", views.profile, name="profile"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Study features
    path("timetable/", views.timetable, name="timetable"),
    path("questions/", views.questions, name="questions"),
    path("progress/", views.progress, name="progress"),

    # Notes
    path("upload-note/", views.upload_note, name="upload_note"),
    path("notes-list/", views.notes_list, name="notes_list"),

    # Success stories
    path("success-stories/", views.success_stories, name="success_stories"),
    path("add-success-story/", views.add_success_story, name="add_success_story"),

    # Study partners
    path("study-profile/", views.study_profile, name="study_profile"),
    path("study-partners/", views.study_partners, name="study_partners"),
    path("partner-requests/", views.partner_requests, name="partner_requests"),
    path("my-partners/", views.my_partners, name="my_partners"),

    # FAQ
    path("faq/", views.faq, name="faq"),
    path("faq/add/", views.add_faq, name="add_faq"),
    path("faq/delete/<int:faq_id>/", views.delete_faq, name="delete_faq"),

    # API
    path("api/auth-check/", views.auth_check, name="auth_check"),
    path("api/success-stories/", views.get_success_stories, name="api_success_stories"),
]
