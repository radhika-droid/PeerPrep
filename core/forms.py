from django import forms
from .models import Contact, SuccessStory, Question, Answer,Goal, Milestone, StudySession, WeeklyGoal,StudyProfile, StudyPartnerRequest,PartnerStudySession
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

class StudyProfileForm(forms.ModelForm):
    class Meta:
        model = StudyProfile
        fields = [
            'bio', 'subjects', 'study_level', 'preferred_study_times', 
            'timezone', 'languages', 'study_goals', 'contact_preference', 
            'contact_info', 'is_available'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Tell others about your study goals, interests, and what you hope to achieve through collaboration...',
                'rows': 4
            }),
            'subjects': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Mathematics, Physics, Computer Science, Biology'
            }),
            'study_level': forms.Select(attrs={
                'class': 'form-input'
            }),
            'preferred_study_times': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., morning, evening, weekend'
            }),
            'timezone': forms.Select(attrs={
                'class': 'form-input'
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., English, Spanish, French'
            }),
            'study_goals': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'What are your current study goals? Exams, projects, skill development...',
                'rows': 3
            }),
            'contact_preference': forms.Select(attrs={
                'class': 'form-input'
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your email, Discord username, etc. (optional)'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }
    
    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects', '')
        if subjects:
            subject_list = [subject.strip() for subject in subjects.split(',') if subject.strip()]
            if len(subject_list) > 10:
                raise forms.ValidationError("Maximum 10 subjects allowed.")
            return ', '.join(subject_list[:10])
        return subjects
    
    def clean_preferred_study_times(self):
        times = self.cleaned_data.get('preferred_study_times', '')
        if times:
            time_list = [time.strip() for time in times.split(',') if time.strip()]
            return ', '.join(time_list[:5])  # Max 5 time preferences
        return times
    
    def clean_languages(self):
        languages = self.cleaned_data.get('languages', '')
        if languages:
            lang_list = [lang.strip() for lang in languages.split(',') if lang.strip()]
            return ', '.join(lang_list[:5])  # Max 5 languages
        return languages


class StudyPartnerRequestForm(forms.ModelForm):
    class Meta:
        model = StudyPartnerRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Introduce yourself and explain why you\'d like to study together. What subjects are you interested in? What are your goals?',
                'rows': 4,
                'required': True
            })
        }
    
    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message.strip()) < 20:
            raise forms.ValidationError("Please provide a more detailed message (at least 20 characters).")
        if len(message) > 300:
            raise forms.ValidationError("Message is too long (maximum 300 characters).")
        return message


class PartnerStudySessionForm(forms.ModelForm):
    class Meta:
        model = PartnerStudySession
        fields = ['title', 'description', 'subject', 'scheduled_time', 'duration_hours']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Calculus Study Session, Physics Problem Solving',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'What will you focus on during this session?',
                'rows': 3
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Mathematics, Physics, Computer Science',
                'required': True
            }),
            'scheduled_time': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local',
                'required': True
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0.5',
                'max': '8.0',
                'step': '0.5',
                'value': '2.0'
            })
        }
    
    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data.get('scheduled_time')
        if scheduled_time:
            from django.utils import timezone
            if scheduled_time <= timezone.now():
                raise forms.ValidationError("Session must be scheduled for a future date and time.")
        return scheduled_time
    
    def clean_duration_hours(self):
        duration = self.cleaned_data.get('duration_hours')
        if duration and (duration < 0.5 or duration > 8.0):
            raise forms.ValidationError("Session duration must be between 0.5 and 8 hours.")
        return duration


class StudyPartnerSearchForm(forms.Form):
    SUBJECT_CHOICES = [
        ('', 'All Subjects'),
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
    
    LEVEL_CHOICES = [
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    TIMEZONE_CHOICES = [
        ('', 'All Timezones'),
        ('UTC-12', 'UTC-12 (Baker Island)'),
        ('UTC-11', 'UTC-11 (American Samoa)'),
        ('UTC-10', 'UTC-10 (Hawaii)'),
        ('UTC-9', 'UTC-9 (Alaska)'),
        ('UTC-8', 'UTC-8 (PST)'),
        ('UTC-7', 'UTC-7 (MST)'),
        ('UTC-6', 'UTC-6 (CST)'),
        ('UTC-5', 'UTC-5 (EST)'),
        ('UTC-4', 'UTC-4 (AST)'),
        ('UTC-3', 'UTC-3 (Brazil)'),
        ('UTC-2', 'UTC-2 (Mid-Atlantic)'),
        ('UTC-1', 'UTC-1 (Azores)'),
        ('UTC+0', 'UTC+0 (GMT/London)'),
        ('UTC+1', 'UTC+1 (CET/Paris)'),
        ('UTC+2', 'UTC+2 (EET/Cairo)'),
        ('UTC+3', 'UTC+3 (Moscow)'),
        ('UTC+4', 'UTC+4 (Dubai)'),
        ('UTC+5', 'UTC+5 (Pakistan)'),
        ('UTC+5:30', 'UTC+5:30 (India)'),
        ('UTC+6', 'UTC+6 (Bangladesh)'),
        ('UTC+7', 'UTC+7 (Thailand)'),
        ('UTC+8', 'UTC+8 (China/Singapore)'),
        ('UTC+9', 'UTC+9 (Japan/Korea)'),
        ('UTC+10', 'UTC+10 (Australia East)'),
        ('UTC+11', 'UTC+11 (Solomon Islands)'),
        ('UTC+12', 'UTC+12 (New Zealand)'),
    ]

    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    
    study_level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    
    timezone = forms.ChoiceField(
        choices=TIMEZONE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Search by name, bio, subjects, or goals...'
        })
    )