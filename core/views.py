from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import SuccessStoryForm   # instead of ContactForm

#from .models import Contact
from .models import SuccessStory
from django.views.decorators.http import require_POST
from django.db.models import F
from .models import SuccessStory, StoryReaction
from .forms import SuccessStoryForm
from .models import StudyNote                    
from django.db.models import Q                   
import os                                       
import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render



def user_login(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Handle AJAX login
            data = request.POST
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid username or password.'})
        else:
            # Handle standard form login (if needed)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'login.html')
    return render(request, 'login.html')

def timetable(request):
    return render(request, "timetable.html")

@require_GET
def auth_check(request):
    """API endpoint to check if user is authenticated"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'user_id': request.user.id if request.user.is_authenticated else None
    })

def index(request):
    form = SuccessStoryForm()

    if request.method == 'POST':
        form = SuccessStoryForm(request.POST)
        if form.is_valid():
            contact = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! Your message has been sent successfully.'
                })
            else:
                messages.success(request, 'Thank you! Your message has been sent successfully.')
                return redirect('index')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    context = {
        'form': form,
    }
    return render(request, 'index.html', context)

def contact_success(request):
    return render(request, 'contact_success.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your submission. Please correct the form fields.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        return render(request, "registration/forgot_password.html", {
            "message": "If details are correct, reset instructions will be sent."
        })
    return render(request, "registration/forgot_password.html")
@login_required
def upload_note(request):
    """
    Allows logged-in users to upload study notes (PDF/DOCX/Images).
    """
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
            return redirect("list_notes")  # redirect to notes list page

    return render(request, "notes/upload_note.html")


def list_notes(request):
    """
    Displays all uploaded notes with filtering and search.
    """
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

    return render(request, "notes/list_notes.html", {"notes": notes, "query": query})


@login_required
def download_note(request, note_id):
    """
    Handles note download and increments download count.
    """
    note = get_object_or_404(StudyNote, id=note_id)

    # increment download count
    note.download_count += 1
    note.save()

    response = FileResponse(note.file.open("rb"), as_attachment=True, filename=note.file.name)
    return response

@login_required
def dashboard(request):
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)

def home(request):
    return render(request, 'home.html')

def feature(request):
    return render(request, 'feature.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# SUCCESS STORIES VIEWS
def success_stories(request):
    """Display success stories page with all published stories"""
    stories = SuccessStory.objects.filter(is_published=True).select_related('user')
    form = SuccessStoryForm() if request.user.is_authenticated else None
    
    context = {
        'stories': stories,
        'form': form,
        'user_is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'successstories.html', context)

@login_required
@require_POST
def add_success_story(request):
    """Handle success story submission via AJAX"""
    try:
        form = SuccessStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()

            return JsonResponse({
                'success': True,
                'message': 'Your success story has been shared successfully!'
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def react_to_story(request, story_id):
    """Handle story reactions (like, heart, celebration)"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            story = get_object_or_404(SuccessStory, id=story_id)
            data = json.loads(request.body)
            reaction_type = data.get('reaction_type')
            
            if reaction_type not in ['like', 'heart', 'celebration']:
                return JsonResponse({'success': False, 'error': 'Invalid reaction type'})
            
            existing_reaction = StoryReaction.objects.filter(
                user=request.user,
                story=story,
                reaction_type=reaction_type
            ).first()
            
            if existing_reaction:
                existing_reaction.delete()
                if reaction_type == 'like':
                    story.likes_count = F('likes_count') - 1
                elif reaction_type == 'heart':
                    story.hearts_count = F('hearts_count') - 1
                elif reaction_type == 'celebration':
                    story.celebrations_count = F('celebrations_count') - 1
                story.save()
                story.refresh_from_db()
                
                return JsonResponse({
                    'success': True,
                    'action': 'removed',
                    'reaction_type': reaction_type,
                    'new_count': getattr(story, f'{reaction_type}s_count')
                })
            else:
                StoryReaction.objects.create(
                    user=request.user,
                    story=story,
                    reaction_type=reaction_type
                )
                if reaction_type == 'like':
                    story.likes_count = F('likes_count') + 1
                elif reaction_type == 'heart':
                    story.hearts_count = F('hearts_count') + 1
                elif reaction_type == 'celebration':
                    story.celebrations_count = F('celebrations_count') + 1
                story.save()
                story.refresh_from_db()
                
                return JsonResponse({
                    'success': True,
                    'action': 'added',
                    'reaction_type': reaction_type,
                    'new_count': getattr(story, f'{reaction_type}s_count')
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def get_user_reactions(request, story_id):
    """Get user's reactions for a specific story"""
    if request.user.is_authenticated:
        reactions = StoryReaction.objects.filter(
            user=request.user,
            story_id=story_id
        ).values_list('reaction_type', flat=True)
        return JsonResponse({'reactions': list(reactions)})
    return JsonResponse({'reactions': []})

def get_success_stories(request):
    """Return all published stories as JSON"""
    stories = SuccessStory.objects.filter(is_published=True).select_related('user')
    stories_data = []

    for story in stories:
        stories_data.append({
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'author_name': story.get_author_name(),
            'user_initials': story.get_user_initials(),
            'category': story.category,
            'tags': story.get_tags_list(),
            'created_at': story.created_at.isoformat(),
            'likes_count': story.likes_count,
            'hearts_count': story.hearts_count,
            'celebrations_count': story.celebrations_count,
        })

    return JsonResponse({'stories': stories_data, 'success': True})
@login_required
@require_POST
def api_create_success_story(request):
    """Handle success story creation via API endpoint"""
    try:
        # Handle both JSON and FormData
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            form = SuccessStoryForm(data)
        else:
            form = SuccessStoryForm(request.POST)
            
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()

            return JsonResponse({
                'success': True,
                'message': 'Your answer has been posted successfully!',
                'answer_id': answer.id
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    
