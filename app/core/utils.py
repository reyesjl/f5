from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

def check_user(user, role):
    """
    Utility function to check if a user has a specific role.
    """
    return user.is_authenticated and user.groups.filter(name=role).exists()

def get_object_or_error(model, **kwargs):
    """
    Utility function to get an object or render an error page if it doesn't exist.
    
    Args:
    - model: The Django model class to query.
    - kwargs: Field lookups for the query.
    
    Returns:
    - object: The retrieved object if found.
    - HttpResponse: Renders an error page if the object is not found.
    """
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        message = f"{model.__name__} with {kwargs} does not exist."
        return render(kwargs.get('request'), "core/error.html", {'message': message})
    except Exception as e:
        message = str(e)
        return render(kwargs.get('request'), "core/error.html", {'message': message})