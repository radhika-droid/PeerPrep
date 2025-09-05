from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']

class SuccessStory(models.Model):
    CATEGORY_CHOICES = [
        ('career', 'Career Growth'),
        ('business', 'Business & Entrepreneurship'),
        ('personal', 'Personal Development'),
        ('health', 'Health & Fitness'),
        ('education', 'Education & Learning'),
        ('creative', 'Creative Pursuits'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='success_stories')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags")
    likes_count = models.PositiveIntegerField(default=0)
    hearts_count = models.PositiveIntegerField(default=0)
    celebrations_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Success Story'
        verbose_name_plural = 'Success Stories'
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def get_user_initials(self):
        """Get user initials for avatar"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        elif self.user.first_name:
            return self.user.first_name[0].upper()
        return self.user.username[0].upper() if self.user.username else "U"
    
    def get_author_name(self):
        """Get display name for author"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        return self.user.username


class StoryReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('heart', 'Heart'),
        ('celebration', 'Celebration'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(SuccessStory, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'story', 'reaction_type')
        
    def __str__(self):
        return f"{self.user.username} {self.reaction_type} {self.story.title}"
    
class Question(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('computer_science', 'Computer Science'),
        ('programming', 'Programming'),
        ('english', 'English'),
        ('history', 'History'),
        ('geography', 'Geography'),
        ('economics', 'Economics'),
        ('psychology', 'Psychology'),
        ('philosophy', 'Philosophy'),
        ('engineering', 'Engineering'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    title = models.CharField(max_length=300)
    description = models.TextField()
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    upvotes_count = models.PositiveIntegerField(default=0)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def get_user_initials(self):
        """Get user initials for avatar"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        elif self.user.first_name:
            return self.user.first_name[0].upper()
        return self.user.username[0].upper() if self.user.username else "U"
    
    def get_author_name(self):
        """Get display name for author"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        return self.user.username
    
    def answers_count(self):
        return self.answers.count()

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    upvotes_count = models.PositiveIntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_accepted', '-upvotes_count', '-created_at']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
    
    def __str__(self):
        return f"Answer by {self.user.username} to '{self.question.title}'"
    
    def get_user_initials(self):
        """Get user initials for avatar"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        elif self.user.first_name:
            return self.user.first_name[0].upper()
        return self.user.username[0].upper() if self.user.username else "U"
    
    def get_author_name(self):
        """Get display name for author"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        return self.user.username

class QuestionUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
        
    def __str__(self):
        return f"{self.user.username} upvoted '{self.question.title}'"

class AnswerUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'answer')
        
    def __str__(self):
        return f"{self.user.username} upvoted answer by {self.answer.user.username}"
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class Goal(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('skill', 'Skill Development'),
        ('career', 'Career'),
        ('personal', 'Personal Growth'),
        ('health', 'Health & Fitness'),
        ('creative', 'Creative'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    target_date = models.DateField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0, help_text="0-100")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        if self.target_date and not self.is_completed:
            return timezone.now().date() > self.target_date
        return False
    
    def days_remaining(self):
        if self.target_date and not self.is_completed:
            delta = self.target_date - timezone.now().date()
            return delta.days
        return None
    
    def save(self, *args, **kwargs):
        if self.progress_percentage >= 100 and not self.is_completed:
            self.is_completed = True
            self.status = 'completed'
            self.completed_at = timezone.now()
        elif self.progress_percentage < 100 and self.is_completed:
            self.is_completed = False
            self.status = 'in_progress'
            self.completed_at = None
        super().save(*args, **kwargs)

class Milestone(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date', 'created_at']
        
    def __str__(self):
        return f"{self.goal.title} - {self.title}"

class StudySession(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('computer_science', 'Computer Science'),
        ('programming', 'Programming'),
        ('english', 'English'),
        ('history', 'History'),
        ('geography', 'Geography'),
        ('economics', 'Economics'),
        ('psychology', 'Psychology'),
        ('philosophy', 'Philosophy'),
        ('engineering', 'Engineering'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    productivity_rating = models.PositiveIntegerField(
        default=5, 
        help_text="1-10 scale"
    )
    goals_related = models.ManyToManyField(Goal, blank=True, related_name='study_sessions')
    notes = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        
    def __str__(self):
        return f"{self.subject} - {self.title} ({self.duration_minutes}min)"

class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('goal_completed', 'Goal Completed'),
        ('streak', 'Study Streak'),
        ('milestone', 'Milestone Reached'),
        ('participation', 'Community Participation'),
        ('helping_others', 'Helping Others'),
        ('consistency', 'Consistency'),
        ('improvement', 'Improvement'),
        ('special', 'Special Achievement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    icon = models.CharField(max_length=10, default='🏆')
    points = models.PositiveIntegerField(default=10)
    is_earned = models.BooleanField(default=True)
    earned_at = models.DateTimeField(auto_now_add=True)
    related_goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-earned_at']
        unique_together = ('user', 'title', 'achievement_type')
        
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_study_hours = models.FloatField(default=0.0)
    total_goals_completed = models.PositiveIntegerField(default=0)
    current_streak_days = models.PositiveIntegerField(default=0)
    longest_streak_days = models.PositiveIntegerField(default=0)
    total_questions_asked = models.PositiveIntegerField(default=0)
    total_answers_given = models.PositiveIntegerField(default=0)
    total_success_stories = models.PositiveIntegerField(default=0)
    achievement_points = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Statistics'
        verbose_name_plural = 'User Statistics'
        
    def __str__(self):
        return f"{self.user.username} - Stats"
    
    def update_streak(self):
        """Update study streak based on recent activity"""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Check if user has activity today or yesterday
        recent_sessions = StudySession.objects.filter(
            user=self.user,
            date__in=[today, yesterday]
        ).exists()
        
        if recent_sessions:
            if self.last_activity_date == yesterday:
                self.current_streak_days += 1
            elif self.last_activity_date != today:
                self.current_streak_days = 1
                
            self.last_activity_date = today
            
            if self.current_streak_days > self.longest_streak_days:
                self.longest_streak_days = self.current_streak_days
        else:
            # Reset streak if no recent activity
            self.current_streak_days = 0
            
        self.save()

class WeeklyGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_goals')
    week_start = models.DateField()
    target_study_hours = models.FloatField(default=10.0)
    target_sessions = models.PositiveIntegerField(default=5)
    actual_study_hours = models.FloatField(default=0.0)
    actual_sessions = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'week_start')
        ordering = ['-week_start']
        
    def __str__(self):
        return f"{self.user.username} - Week of {self.week_start}"
    
    def progress_percentage(self):
        hours_progress = min((self.actual_study_hours / self.target_study_hours) * 100, 100) if self.target_study_hours > 0 else 100
        sessions_progress = min((self.actual_sessions / self.target_sessions) * 100, 100) if self.target_sessions > 0 else 100
        return (hours_progress + sessions_progress) / 2