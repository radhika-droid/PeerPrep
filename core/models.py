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