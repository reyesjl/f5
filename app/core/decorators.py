from functools import wraps
from django.shortcuts import render

def is_admin(user):
    # Or use user.has_perm('your_permission') for custom permissions
    return user.is_staff