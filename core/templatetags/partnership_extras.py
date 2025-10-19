# Create these files for custom template filters

# 1. Create core/templatetags/__init__.py (empty file)

# 2. Create core/templatetags/partnership_extras.py
from django import template

register = template.Library()

@register.filter
def get_partner(partnership, current_user):
    """Get the other user in the partnership"""
    return partnership.user2 if partnership.user1 == current_user else partnership.user1

@register.filter 
def get_display_name_safe(user):
    """Safely get display name for JavaScript"""
    if hasattr(user, 'study_profile') and user.study_profile:
        return user.study_profile.get_display_name()
    return user.username