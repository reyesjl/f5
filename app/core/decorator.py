from functools import wraps
from django.shortcuts import render

def user_has_role(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=role).exists():
                return view_func(request, *args, **kwargs)
            else:
                message = "Permission denied: user does not have the correct role(s) to view this page."
                return render(request, "core/permission_denied.html", {"message": message}, status=403)
        return wrapped_view
    return decorator