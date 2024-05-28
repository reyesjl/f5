from django.contrib.auth.models import Group

def check_user(user, role):
    """
    Utility function to check if a user has a specific role.
    """
    return user.is_authenticated and user.groups.filter(name=role).exists()