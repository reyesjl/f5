import uuid
from functools import wraps
from django.shortcuts import render

def validate_rsvp_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            # Attempt to parse the token as a UUID
            uuid_obj = uuid.UUID(token)
        except ValueError:
            # If parsing fails, token is not a valid UUID, return invalid template
            return render(request, 'events/rsvp_invalid_token.html')
        
        # If parsing succeeds, continue executing the view function
        return view_func(request, *args, **kwargs)

    return _wrapped_view