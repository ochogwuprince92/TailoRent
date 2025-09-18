# backend/profiles/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def replace(value, args):
    """Usage: {{ value|replace:"old,new" }} replaces 'old' with 'new' in the string."""
    try:
        old, new = args.split(',')
        return value.replace(old, new)
    except ValueError:
        return value  # If there's an error, just return the original
