from django import forms
from .models import Contact, SuccessStory, Question, Answer,Goal, Milestone, StudySession, WeeklyGoal
from .models import FAQ
from django.utils import timezone
from datetime import datetime, timedelta

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your phone number'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': "What's this about?",
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Tell us more about how we can help you...',
                'required': True
            }),
        }
class SuccessStoryForm(forms.ModelForm):
    class Meta:
        model = SuccessStory
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., From Zero to Hero: My Coding Journey'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Share your journey, challenges you overcame, and what you learned...',
                'rows': 6
            }),
            'category': forms.Select(attrs={
                'class': 'form-input'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Career Growth, Technology, Entrepreneurship (separate with commas)'
            }),
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if len(tag_list) > 10:
                raise forms.ValidationError("Maximum 10 tags allowed.")
            return ', '.join(tag_list[:10])
        return tags
    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'title', 'description', 'tags']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., How to solve quadratic equations?',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Provide detailed description of your question...',
                'rows': 5,
                'required': True
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., algebra, equations, homework (separate with commas)'
            }),
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if len(tag_list) > 15:
                raise forms.ValidationError("Maximum 15 tags allowed.")
            return ', '.join(tag_list[:15])
        return tags

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Share your answer and explanation...',
                'rows': 4,
                'required': True
            }),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        if len(content.strip()) < 10:
            raise forms.ValidationError("Answer must be at least 10 characters long.")
        return content
class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'category', 'priority', 'target_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Master Python Programming',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe your goal in detail...',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'target_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }
    
    def clean_target_date(self):
        target_date = self.cleaned_data.get('target_date')
        if target_date and target_date <= timezone.now().date():
            raise forms.ValidationError("Target date must be in the future.")
        return target_date

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Complete Chapter 1',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe this milestone...',
                'rows': 2
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['subject', 'title', 'description', 'duration_minutes', 'productivity_rating', 'notes', 'date']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Algebra Practice Session',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'What did you study?',
                'rows': 2
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '60',
                'min': '1',
                'max': '480',
                'required': True
            }),
            'productivity_rating': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'max': '10',
                'value': '5',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Any notes or reflections...',
                'rows': 3
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'value': timezone.now().date()
            }),
        }
    
    def clean_duration_minutes(self):
        duration = self.cleaned_data.get('duration_minutes')
        if duration and (duration < 1 or duration > 480):
            raise forms.ValidationError("Duration must be between 1 and 480 minutes (8 hours).")
        return duration
    
    def clean_productivity_rating(self):
        rating = self.cleaned_data.get('productivity_rating')
        if rating and (rating < 1 or rating > 10):
            raise forms.ValidationError("Productivity rating must be between 1 and 10.")
        return rating
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise forms.ValidationError("Study session date cannot be in the future.")
        return date

class WeeklyGoalForm(forms.ModelForm):
    class Meta:
        model = WeeklyGoal
        fields = ['target_study_hours', 'target_sessions']
        widgets = {
            'target_study_hours': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '10.0',
                'step': '0.5',
                'min': '0.5',
                'max': '60',
                'required': True
            }),
            'target_sessions': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '5',
                'min': '1',
                'max': '20',
                'required': True
            }),
        }
    
    def clean_target_study_hours(self):
        hours = self.cleaned_data.get('target_study_hours')
        if hours and (hours < 0.5 or hours > 60):
            raise forms.ValidationError("Target study hours must be between 0.5 and 60 hours per week.")
        return hours
    
    def clean_target_sessions(self):
        sessions = self.cleaned_data.get('target_sessions')
        if sessions and (sessions < 1 or sessions > 20):
            raise forms.ValidationError("Target sessions must be between 1 and 20 sessions per week.")
        return sessions

class GoalUpdateForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['progress_percentage', 'status']
        widgets = {
            'progress_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '100',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
        }