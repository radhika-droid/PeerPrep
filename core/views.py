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
from .models import FAQ
from .forms import FAQForm 
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import Goal, Milestone, StudySession, Achievement, UserStats, WeeklyGoal
from .forms import GoalForm, MilestoneForm, StudySessionForm, WeeklyGoalForm, GoalUpdateForm

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
def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

# Only allow superusers
@user_passes_test(lambda u: u.is_superuser)
def add_faq(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq')
    else:
        form = FAQForm()
    return render(request, 'add_faq.html', {'form': form})
@user_passes_test(lambda u: u.is_superuser)
def delete_faq(request, faq_id):
    faq = FAQ.objects.get(id=faq_id)
    faq.delete()
    return redirect('faq')

@login_required
def progress_tracking(request):
    """Main progress tracking dashboard"""
    return render(request, 'progress.html')

@login_required
def get_progress_dashboard_data(request):
    """Get all dashboard data in one API call"""
    try:
        user = request.user
        
        # Get or create user stats
        stats, created = UserStats.objects.get_or_create(user=user)
        if created:
            stats.update_streak()
        
        # Goals data
        goals = Goal.objects.filter(user=user)
        total_goals = goals.count()
        completed_goals = goals.filter(is_completed=True).count()
        active_goals = goals.filter(status='in_progress').count()
        overdue_goals = goals.filter(
            target_date__lt=timezone.now().date(),
            is_completed=False
        ).count()
        
        # Recent study sessions
        recent_sessions = StudySession.objects.filter(
            user=user,
            date__gte=timezone.now().date() - timedelta(days=7)
        ).order_by('-date', '-created_at')[:5]
        
        # Weekly progress
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        current_week, created = WeeklyGoal.objects.get_or_create(
            user=user,
            week_start=week_start,
            defaults={'target_study_hours': 10.0, 'target_sessions': 5}
        )
        
        # Calculate actual weekly progress
        week_sessions = StudySession.objects.filter(
            user=user,
            date__gte=week_start,
            date__lt=week_start + timedelta(days=7)
        )
        current_week.actual_study_hours = sum(session.duration_minutes for session in week_sessions) / 60.0
        current_week.actual_sessions = week_sessions.count()
        current_week.save()
        
        # Recent achievements
        recent_achievements = Achievement.objects.filter(user=user).order_by('-earned_at')[:5]
        
        # Study time by subject (last 30 days)
        subject_data = StudySession.objects.filter(
            user=user,
            date__gte=timezone.now().date() - timedelta(days=30)
        ).values('subject').annotate(
            total_minutes=Sum('duration_minutes'),
            session_count=Count('id')
        ).order_by('-total_minutes')
        
        # Daily study time (last 7 days)
        daily_data = []
        for i in range(6, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            day_sessions = StudySession.objects.filter(user=user, date=date)
            total_minutes = sum(session.duration_minutes for session in day_sessions)
            daily_data.append({
                'date': date.isoformat(),
                'day': date.strftime('%a'),
                'hours': round(total_minutes / 60.0, 1),
                'sessions': day_sessions.count()
            })
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_study_hours': round(stats.total_study_hours, 1),
                'total_goals_completed': stats.total_goals_completed,
                'current_streak_days': stats.current_streak_days,
                'achievement_points': stats.achievement_points,
                'total_goals': total_goals,
                'active_goals': active_goals,
                'overdue_goals': overdue_goals,
            },
            'weekly_progress': {
                'target_hours': current_week.target_study_hours,
                'actual_hours': round(current_week.actual_study_hours, 1),
                'target_sessions': current_week.target_sessions,
                'actual_sessions': current_week.actual_sessions,
                'progress_percentage': round(current_week.progress_percentage(), 1)
            },
            'recent_sessions': [{
                'id': session.id,
                'title': session.title,
                'subject': session.get_subject_display(),
                'duration_minutes': session.duration_minutes,
                'productivity_rating': session.productivity_rating,
                'date': session.date.isoformat(),
            } for session in recent_sessions],
            'recent_achievements': [{
                'title': achievement.title,
                'description': achievement.description,
                'icon': achievement.icon,
                'points': achievement.points,
                'earned_at': achievement.earned_at.isoformat(),
            } for achievement in recent_achievements],
            'subject_data': [{
                'subject': item['subject'],
                'subject_display': dict(StudySession.SUBJECT_CHOICES)[item['subject']],
                'hours': round(item['total_minutes'] / 60.0, 1),
                'sessions': item['session_count']
            } for item in subject_data],
            'daily_data': daily_data
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_goals(request):
    """Get user's goals"""
    try:
        goals = Goal.objects.filter(user=request.user).prefetch_related('milestones')
        goals_data = []
        
        for goal in goals:
            goals_data.append({
                'id': goal.id,
                'title': goal.title,
                'description': goal.description,
                'category': goal.category,
                'category_display': goal.get_category_display(),
                'priority': goal.priority,
                'priority_display': goal.get_priority_display(),
                'status': goal.status,
                'status_display': goal.get_status_display(),
                'progress_percentage': goal.progress_percentage,
                'target_date': goal.target_date.isoformat() if goal.target_date else None,
                'is_completed': goal.is_completed,
                'is_overdue': goal.is_overdue(),
                'days_remaining': goal.days_remaining(),
                'created_at': goal.created_at.isoformat(),
                'milestones_count': goal.milestones.count(),
                'completed_milestones': goal.milestones.filter(is_completed=True).count(),
            })
        
        return JsonResponse({'success': True, 'goals': goals_data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def create_goal(request):
    """Create a new goal"""
    try:
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Goal created successfully!',
                'goal_id': goal.id
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def update_goal_progress(request, goal_id):
    """Update goal progress"""
    try:
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        data = json.loads(request.body)
        
        progress = data.get('progress_percentage', goal.progress_percentage)
        status = data.get('status', goal.status)
        
        if not (0 <= progress <= 100):
            return JsonResponse({'success': False, 'error': 'Progress must be between 0 and 100'})
        
        goal.progress_percentage = progress
        goal.status = status
        goal.save()
        
        # Check for achievements
        if goal.is_completed and not Achievement.objects.filter(
            user=request.user,
            achievement_type='goal_completed',
            related_goal=goal
        ).exists():
            Achievement.objects.create(
                user=request.user,
                title=f'Goal Completed: {goal.title}',
                description=f'Successfully completed the goal "{goal.title}"',
                achievement_type='goal_completed',
                icon='🎯',
                points=20,
                related_goal=goal
            )
            
            # Update user stats
            stats, created = UserStats.objects.get_or_create(user=request.user)
            stats.total_goals_completed += 1
            stats.achievement_points += 20
            stats.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Goal updated successfully!',
            'is_completed': goal.is_completed
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def log_study_session(request):
    """Log a new study session"""
    try:
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            
            # Update user stats
            stats, created = UserStats.objects.get_or_create(user=request.user)
            stats.total_study_hours += session.duration_minutes / 60.0
            stats.update_streak()
            stats.save()
            
            # Check for streak achievements
            if stats.current_streak_days in [7, 14, 30, 60, 100] and not Achievement.objects.filter(
                user=request.user,
                title=f'{stats.current_streak_days} Day Study Streak'
            ).exists():
                Achievement.objects.create(
                    user=request.user,
                    title=f'{stats.current_streak_days} Day Study Streak',
                    description=f'Maintained a {stats.current_streak_days} day study streak!',
                    achievement_type='streak',
                    icon='🔥',
                    points=stats.current_streak_days // 7 * 10
                )
                stats.achievement_points += stats.current_streak_days // 7 * 10
                stats.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Study session logged successfully!',
                'session_id': session.id
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_analytics_data(request):
    """Get detailed analytics data"""
    try:
        user = request.user
        
        # Time range for analysis
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Study patterns
        sessions = StudySession.objects.filter(
            user=user,
            date__gte=start_date
        )
        
        # Productivity trends
        productivity_by_day = []
        for i in range(29, -1, -1):
            date = end_date - timedelta(days=i)
            day_sessions = sessions.filter(date=date)
            avg_productivity = day_sessions.aggregate(
                avg=Avg('productivity_rating')
            )['avg'] or 0
            total_minutes = sum(s.duration_minutes for s in day_sessions)
            
            productivity_by_day.append({
                'date': date.isoformat(),
                'day': date.strftime('%a'),
                'productivity': round(avg_productivity, 1),
                'study_time': round(total_minutes / 60.0, 1),
                'sessions': day_sessions.count()
            })
        
        # Subject distribution
        subject_stats = sessions.values('subject').annotate(
            total_minutes=Sum('duration_minutes'),
            session_count=Count('id'),
            avg_productivity=Avg('productivity_rating')
        ).order_by('-total_minutes')
        
        # Goal completion rates by category
        goal_stats = Goal.objects.filter(user=user).values('category').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(is_completed=True)),
            avg_progress=Avg('progress_percentage')
        ).order_by('-total')
        
        # Monthly comparison
        this_month_start = end_date.replace(day=1)
        last_month_end = this_month_start - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        
        this_month_sessions = StudySession.objects.filter(
            user=user,
            date__gte=this_month_start
        )
        last_month_sessions = StudySession.objects.filter(
            user=user,
            date__gte=last_month_start,
            date__lte=last_month_end
        )
        
        this_month_hours = sum(s.duration_minutes for s in this_month_sessions) / 60.0
        last_month_hours = sum(s.duration_minutes for s in last_month_sessions) / 60.0
        
        return JsonResponse({
            'success': True,
            'productivity_trends': productivity_by_day,
            'subject_distribution': [{
                'subject': item['subject'],
                'subject_display': dict(StudySession.SUBJECT_CHOICES)[item['subject']],
                'hours': round(item['total_minutes'] / 60.0, 1),
                'sessions': item['session_count'],
                'avg_productivity': round(item['avg_productivity'], 1),
                'percentage': round((item['total_minutes'] / sum(s['total_minutes'] for s in subject_stats)) * 100, 1) if subject_stats else 0
            } for item in subject_stats],
            'goal_completion': [{
                'category': item['category'],
                'category_display': dict(Goal.CATEGORY_CHOICES)[item['category']],
                'total': item['total'],
                'completed': item['completed'],
                'completion_rate': round((item['completed'] / item['total']) * 100, 1) if item['total'] > 0 else 0,
                'avg_progress': round(item['avg_progress'], 1)
            } for item in goal_stats],
            'monthly_comparison': {
                'this_month': {
                    'hours': round(this_month_hours, 1),
                    'sessions': this_month_sessions.count(),
                    'avg_productivity': round(this_month_sessions.aggregate(avg=Avg('productivity_rating'))['avg'] or 0, 1)
                },
                'last_month': {
                    'hours': round(last_month_hours, 1),
                    'sessions': last_month_sessions.count(),
                    'avg_productivity': round(last_month_sessions.aggregate(avg=Avg('productivity_rating'))['avg'] or 0, 1)
                },
                'change': {
                    'hours': round(this_month_hours - last_month_hours, 1),
                    'sessions': this_month_sessions.count() - last_month_sessions.count()
                }
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def set_weekly_goal(request):
    """Set or update weekly goals"""
    try:
        data = json.loads(request.body)
        target_hours = float(data.get('target_hours', 10))
        target_sessions = int(data.get('target_sessions', 5))
        
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        weekly_goal, created = WeeklyGoal.objects.update_or_create(
            user=request.user,
            week_start=week_start,
            defaults={
                'target_study_hours': target_hours,
                'target_sessions': target_sessions
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Weekly goals updated successfully!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def delete_goal(request, goal_id):
    """Delete a goal"""
    try:
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Goal deleted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_goal_detail(request, goal_id):
    """Get detailed goal information with milestones"""
    try:
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        milestones = goal.milestones.all()
        
        goal_data = {
            'id': goal.id,
            'title': goal.title,
            'description': goal.description,
            'category': goal.category,
            'priority': goal.priority,
            'status': goal.status,
            'progress_percentage': goal.progress_percentage,
            'target_date': goal.target_date.isoformat() if goal.target_date else None,
            'is_completed': goal.is_completed,
            'is_overdue': goal.is_overdue(),
            'days_remaining': goal.days_remaining(),
            'created_at': goal.created_at.isoformat(),
            'milestones': [{
                'id': milestone.id,
                'title': milestone.title,
                'description': milestone.description,
                'is_completed': milestone.is_completed,
                'due_date': milestone.due_date.isoformat() if milestone.due_date else None,
                'completed_at': milestone.completed_at.isoformat() if milestone.completed_at else None,
            } for milestone in milestones]
        }
        
        return JsonResponse({
            'success': True,
            'goal': goal_data
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def create_milestone(request, goal_id):
    """Create a milestone for a goal"""
    try:
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        form = MilestoneForm(request.POST)
        
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.goal = goal
            milestone.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Milestone created successfully!',
                'milestone_id': milestone.id
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def toggle_milestone(request, milestone_id):
    """Toggle milestone completion status"""
    try:
        milestone = get_object_or_404(Milestone, id=milestone_id, goal__user=request.user)
        
        milestone.is_completed = not milestone.is_completed
        if milestone.is_completed:
            milestone.completed_at = timezone.now()
        else:
            milestone.completed_at = None
        milestone.save()
        
        return JsonResponse({
            'success': True,
            'is_completed': milestone.is_completed,
            'message': f'Milestone {"completed" if milestone.is_completed else "reopened"}!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_recent_activity(request):
    """Get recent user activity for the activity feed"""
    try:
        user = request.user
        activities = []
        
        # Recent study sessions
        recent_sessions = StudySession.objects.filter(user=user).order_by('-created_at')[:5]
        for session in recent_sessions:
            activities.append({
                'type': 'study_session',
                'title': f'Studied {session.get_subject_display()}',
                'description': f'{session.title} for {session.duration_minutes} minutes',
                'timestamp': session.created_at.isoformat(),
                'icon': '📚'
            })
        
        # Recent goal updates
        recent_goals = Goal.objects.filter(user=user, updated_at__gte=timezone.now() - timedelta(days=7)).order_by('-updated_at')[:5]
        for goal in recent_goals:
            if goal.is_completed:
                activities.append({
                    'type': 'goal_completed',
                    'title': f'Completed Goal: {goal.title}',
                    'description': f'Successfully achieved your {goal.get_category_display().lower()} goal',
                    'timestamp': goal.updated_at.isoformat(),
                    'icon': '🎯'
                })
        
        # Recent achievements
        recent_achievements = Achievement.objects.filter(user=user).order_by('-earned_at')[:5]
        for achievement in recent_achievements:
            activities.append({
                'type': 'achievement',
                'title': f'Achievement Unlocked: {achievement.title}',
                'description': achievement.description,
                'timestamp': achievement.earned_at.isoformat(),
                'icon': achievement.icon,
                'points': achievement.points
            })
        
        # Sort all activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return JsonResponse({
            'success': True,
            'activities': activities[:10]  # Return top 10 most recent
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})