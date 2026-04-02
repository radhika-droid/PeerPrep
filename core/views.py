from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Q, F
from .models import SuccessStory, StoryReaction, StudyNote
from .forms import SuccessStoryForm
import json
from .models import FAQ

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def feature(request):
    return render(request, "feature.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def contact_success(request):
    return render(request, "contact_success.html")

def register(request):
    from django.contrib.auth.forms import UserCreationForm
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Error creating account")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def profile(request):
    return render(request, "profile.html")

def faq(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order', '-created_at')
    return render(request, "faq.html", {"faqs": faqs})
@login_required
def add_faq(request):
    if not request.user.is_superuser:
        return redirect("faq")
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        answer = request.POST.get("answer", "").strip()
        if question and answer:
            FAQ.objects.create(question=question, answer=answer)
            messages.success(request, "FAQ added successfully!")
        return redirect("faq")
    return redirect("faq")

@login_required  
def delete_faq(request, faq_id):
    if not request.user.is_superuser:
        return redirect("faq")
    faq_obj = get_object_or_404(FAQ, id=faq_id)
    faq_obj.delete()
    messages.success(request, "FAQ deleted.")
    return redirect("faq")


@login_required
def questions(request):
    return render(request, "questions.html")

@login_required
def timetable(request):
    return render(request, "timetable.html")

@login_required
def progress(request):
    return render(request, "progress.html")

# Notes
@login_required
def upload_note(request):
    if request.method == "POST":
        title = request.POST.get("title")
        subject = request.POST.get("subject")
        file = request.FILES.get("file")
        if title and subject and file:
            StudyNote.objects.create(
                title=title,
                subject=subject,
                file=file,
                uploader=request.user,
            )
            return redirect("notes_list")
    return render(request, "notes/upload_note.html")

def notes_list(request):
    query = request.GET.get("q", "")
    subject_filter = request.GET.get("subject", "")
    notes = StudyNote.objects.all()
    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(uploader__username__icontains=query)
        )
    if subject_filter:
        notes = notes.filter(subject__icontains=subject_filter)
    return render(request, "notes/list_notes.html", {"notes": notes})

# Success Stories
def success_stories(request):
    stories = SuccessStory.objects.filter(is_published=True)
    form = SuccessStoryForm()
    return render(request, "successstories.html", {
        "stories": stories,
        "form": form
    })

@login_required
def add_success_story(request):
    if request.method == "POST":
        form = SuccessStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect("success_stories")
    return redirect("success_stories")

def get_success_stories(request):
    stories = SuccessStory.objects.filter(is_published=True)
    return JsonResponse({"stories": [
        {
            "id": s.id,
            "title": s.title,
            "content": s.content,
            "likes": s.likes_count,
        }
        for s in stories
    ]})

# Study Partners
@login_required
def study_profile(request):
    return render(request, "study_profile.html")

@login_required
def study_partners(request):
    return render(request, "study_partners.html")

@login_required
def partner_requests(request):
    return render(request, "partner_requests.html")

@login_required
def my_partners(request):
    return render(request, "my_partners.html")

# API Auth Check
def auth_check(request):
    return JsonResponse({"authenticated": request.user.is_authenticated})

def forgot_password(request):
    return render(request, "forgot_password.html")

def logged_out(request):
    return render(request, "registration/logged_out.html")


