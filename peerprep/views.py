from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm

# ----------------------
# Basic Pages
# ----------------------

def index(request):
    return render(request, "index.html")

def contact_success(request):
    return render(request, "contact_success.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "register.html", {"error": "Username already exists"})
    return render(request, "register.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

def home(request):
    return render(request, "home.html")

def feature(request):
    return render(request, "feature.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def forgot_password(request):
    return render(request, "forgot_password.html")

# ----------------------
# Success Stories Section
# ----------------------

success_stories_data = []  # temporary in-memory store

def success_stories(request):
    return render(request, "success_stories.html", {"stories": success_stories_data})

@csrf_exempt
def add_success_story(request):
    if request.method == "POST":
        story_text = request.POST.get("story")
        if story_text:
            new_story = {"id": len(success_stories_data) + 1, "text": story_text, "reactions": {}}
            success_stories_data.append(new_story)
            return redirect("success_stories")
    return render(request, "add_success_story.html")

@csrf_exempt
def react_to_story(request, story_id):
    if request.method == "POST":
        reaction = request.POST.get("reaction")
        username = request.user.username if request.user.is_authenticated else "Anonymous"

        for story in success_stories_data:
            if story["id"] == story_id:
                story["reactions"][username] = reaction
                return JsonResponse({"status": "success", "story": story})
    return JsonResponse({"status": "error", "message": "Invalid request"})

def get_user_reactions(request, story_id):
    for story in success_stories_data:
        if story["id"] == story_id:
            return JsonResponse({"reactions": story["reactions"]})
    return JsonResponse({"error": "Story not found"})

def get_success_stories(request):
    return JsonResponse({"stories": success_stories_data})

# ----------------------
# Auth Check (for frontend)
# ----------------------

def auth_check(request):
    return JsonResponse({"is_authenticated": request.user.is_authenticated})
