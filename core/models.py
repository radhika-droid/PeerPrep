from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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


class StudyNote(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('cs', 'Computer Science'),
        ('ds', 'Data Structures'),
        ('algorithms', 'Algorithms'),
        ('web', 'Web Development'),
        ('ml', 'Machine Learning'),
        ('db', 'Databases'),
        ('os', 'Operating Systems'),
        ('networking', 'Networking'),
        ('other', 'Other'),
    ]
    is_verified = models.BooleanField(default=False)

    title = models.CharField(max_length=200, help_text="Title of your study notes")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, help_text="Subject of the notes")
    topic = models.CharField(max_length=100, blank=True, help_text="Specific topic (e.g., Binary Search)")
    description = models.TextField(blank=True, help_text="Brief description of the notes")

    # File upload
    file = models.FileField(upload_to='study_notes/', help_text="Upload PDF, DOCX, or image files")
    thumbnail = models.ImageField(upload_to='note_thumbnails/', blank=True, null=True, help_text="Optional thumbnail image")

    # Metadata
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_notes')
    upload_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Visibility settings
    is_approved = models.BooleanField(default=True, help_text="Whether the note is approved for sharing")
    is_public = models.BooleanField(default=True, help_text="Whether the note is visible to all users")

    # Track downloads
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Study Note'
        verbose_name_plural = 'Study Notes'

    def __str__(self):
        return f"{self.title} by {self.uploader.username}"

    def get_file_extension(self):
        """Return file extension in lowercase"""
        if self.file:
            return self.file.name.split('.')[-1].lower()
        return ''

    def is_pdf(self):
        return self.get_file_extension() == 'pdf'

    def is_image(self):
        ext = self.get_file_extension()
        return ext in ['png', 'jpg', 'jpeg', 'gif']

    def is_docx(self):
        return self.get_file_extension() == 'docx'

    def get_uploader_name(self):
        """Get display name for uploader"""
        user = self.uploader
        if user.first_name and user.last_name:
            return f"{user.first_name} {user.last_name}"
        elif user.first_name:
            return user.first_name
        return user.username


# FAQ Model
class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return self.question


# Q&A Forum Models
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=300)
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True)
    upvotes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_accepted', '-upvotes', '-created_at']
    
    def __str__(self):
        return f"Answer to {self.question.title} by {self.user.username}"


class QuestionUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='upvote_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
    
    def __str__(self):
        return f"{self.user.username} upvoted {self.question.title}"


class AnswerUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='upvote_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'answer')
    
    def __str__(self):
        return f"{self.user.username} upvoted answer"


# Study Tracker Models
class Goal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    target_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    current_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def progress_percentage(self):
        if self.target_hours > 0:
            return min(100, (float(self.current_hours) / float(self.target_hours)) * 100)
        return 0


class Milestone(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.goal.title} - {self.title}"


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    notes = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subject} ({self.duration_minutes}min)"


class Achievement(models.Model):
    ACHIEVEMENT_TYPE_CHOICES = [
        ('streak', 'Streak'),
        ('hours', 'Study Hours'),
        ('sessions', 'Study Sessions'),
        ('goals', 'Goals Completed'),
        ('special', 'Special'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)
    icon = models.CharField(max_length=50, blank=True)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_study_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sessions = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    goals_completed = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Stats'
        verbose_name_plural = 'User Stats'
    
    def __str__(self):
        return f"{self.user.username} Stats"


class WeeklyGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_goals')
    week_start = models.DateField()
    target_hours = models.DecimalField(max_digits=5, decimal_places=2)
    current_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-week_start']
        unique_together = ('user', 'week_start')
    
    def __str__(self):
        return f"{self.user.username} - Week of {self.week_start}"


class StudyProfile(models.Model):
    STUDY_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='study_profile')
    bio = models.TextField(blank=True)
    study_level = models.CharField(max_length=20, choices=STUDY_LEVEL_CHOICES, default='beginner')
    subjects_of_interest = models.CharField(max_length=300, blank=True)
    preferred_study_time = models.CharField(max_length=100, blank=True)
    study_goals = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


# Study Partner Models
class StudyPartnerRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_partner_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_partner_requests')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"


class StudyPartnership(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partnerships_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partnerships_as_user2')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
    
    def __str__(self):
        return f"{self.user1.username} & {self.user2.username}"


class PartnerStudySession(models.Model):
    partnership = models.ForeignKey(StudyPartnership, on_delete=models.CASCADE, related_name='sessions')
    subject = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    notes = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.partnership} - {self.subject} ({self.date})"