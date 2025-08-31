from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ContactForm, SuccessStoryForm, QuestionForm, AnswerForm
from .models import Contact, SuccessStory, StoryReaction, Question, Answer, QuestionUpvote, AnswerUpvote
from django.views.decorators.http import require_POST, require_GET
from django.db.models import F
import json
from django.contrib.auth import authenticate, login

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
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
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
def questions(request):
    """Display questions page"""
    context = {
        'user_is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'questions.html', context)

@login_required
@require_POST
def ask_question(request):
    """Handle question submission via AJAX"""
    try:
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

            return JsonResponse({
                'success': True,
                'message': 'Your question has been posted successfully!',
                'question_id': question.id
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

def get_questions(request):
    """Return all questions as JSON"""
    questions = Question.objects.select_related('user').prefetch_related('answers')
    questions_data = []

    for question in questions:
        # Check if current user has upvoted this question
        user_upvoted = False
        if request.user.is_authenticated:
            user_upvoted = QuestionUpvote.objects.filter(
                user=request.user,
                question=question
            ).exists()

        questions_data.append({
            'id': question.id,
            'title': question.title,
            'description': question.description,
            'subject': question.subject,
            'author_name': question.get_author_name(),
            'user_initials': question.get_user_initials(),
            'user_id': question.user.id,
            'tags': question.get_tags_list(),
            'created_at': question.created_at.isoformat(),
            'upvotes_count': question.upvotes_count,
            'answers_count': question.answers_count(),
            'is_solved': question.is_solved,
            'user_upvoted': user_upvoted,
        })

    return JsonResponse({'questions': questions_data, 'success': True})

def get_question_detail(request, question_id):
    """Get detailed question with answers"""
    try:
        question = get_object_or_404(Question, id=question_id)
        answers = Answer.objects.filter(question=question).select_related('user')
        
        # Check if current user has upvoted this question
        user_upvoted = False
        if request.user.is_authenticated:
            user_upvoted = QuestionUpvote.objects.filter(
                user=request.user,
                question=question
            ).exists()

        question_data = {
            'id': question.id,
            'title': question.title,
            'description': question.description,
            'subject': question.subject,
            'author_name': question.get_author_name(),
            'user_initials': question.get_user_initials(),
            'user_id': question.user.id,
            'tags': question.get_tags_list(),
            'created_at': question.created_at.isoformat(),
            'upvotes_count': question.upvotes_count,
            'is_solved': question.is_solved,
            'user_upvoted': user_upvoted,
        }

        answers_data = []
        for answer in answers:
            # Check if current user has upvoted this answer
            answer_user_upvoted = False
            if request.user.is_authenticated:
                answer_user_upvoted = AnswerUpvote.objects.filter(
                    user=request.user,
                    answer=answer
                ).exists()

            answers_data.append({
                'id': answer.id,
                'content': answer.content,
                'author_name': answer.get_author_name(),
                'user_initials': answer.get_user_initials(),
                'user_id': answer.user.id,
                'created_at': answer.created_at.isoformat(),
                'upvotes_count': answer.upvotes_count,
                'is_accepted': answer.is_accepted,
                'user_upvoted': answer_user_upvoted,
            })

        return JsonResponse({
            'success': True,
            'question': question_data,
            'answers': answers_data
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def answer_question(request, question_id):
    """Handle answer submission via AJAX"""
    try:
        question = get_object_or_404(Question, id=question_id)
        form = AnswerForm(request.POST)
        
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

@login_required
@require_POST
def upvote_question(request, question_id):
    """Handle question upvoting"""
    try:
        question = get_object_or_404(Question, id=question_id)
        
        existing_upvote = QuestionUpvote.objects.filter(
            user=request.user,
            question=question
        ).first()
        
        if existing_upvote:
            existing_upvote.delete()
            question.upvotes_count = F('upvotes_count') - 1
            question.save()
            question.refresh_from_db()
            
            return JsonResponse({
                'success': True,
                'action': 'removed',
                'new_count': question.upvotes_count
            })
        else:
            QuestionUpvote.objects.create(
                user=request.user,
                question=question
            )
            question.upvotes_count = F('upvotes_count') + 1
            question.save()
            question.refresh_from_db()
            
            return JsonResponse({
                'success': True,
                'action': 'added',
                'new_count': question.upvotes_count
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def upvote_answer(request, answer_id):
    """Handle answer upvoting"""
    try:
        answer = get_object_or_404(Answer, id=answer_id)
        
        existing_upvote = AnswerUpvote.objects.filter(
            user=request.user,
            answer=answer
        ).first()
        
        if existing_upvote:
            existing_upvote.delete()
            answer.upvotes_count = F('upvotes_count') - 1
            answer.save()
            answer.refresh_from_db()
            
            return JsonResponse({
                'success': True,
                'action': 'removed',
                'new_count': answer.upvotes_count
            })
        else:
            AnswerUpvote.objects.create(
                user=request.user,
                answer=answer
            )
            answer.upvotes_count = F('upvotes_count') + 1
            answer.save()
            answer.refresh_from_db()
            
            return JsonResponse({
                'success': True,
                'action': 'added',
                'new_count': answer.upvotes_count
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def accept_answer(request, answer_id):
    """Handle accepting an answer as the solution"""
    try:
        answer = get_object_or_404(Answer, id=answer_id)
        question = answer.question
        
        if question.user != request.user:
            return JsonResponse({
                'success': False,
                'error': 'Only the question author can accept answers'
            }, status=403)
        
        if question.is_solved:
            return JsonResponse({
                'success': False,
                'error': 'This question already has an accepted answer'
            })
        
        answer.is_accepted = True
        answer.save()
        
        question.is_solved = True
        question.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Answer accepted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})