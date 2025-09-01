from django import forms
from .models import Contact, SuccessStory, Question, Answer
from .models import FAQ

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