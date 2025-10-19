from django import forms

class SuccessStoryForm(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    category = forms.ChoiceField(
        choices=[("Academic", "Academic"), ("Career", "Career")],
        required=True
    )
    tags = forms.CharField(required=False, help_text="Comma-separated tags")

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", "")
        # Validate tags: remove extra spaces, no empty tags
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        return tag_list
