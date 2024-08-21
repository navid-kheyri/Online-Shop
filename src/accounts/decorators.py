from functools import wraps
from django.http import HttpResponseForbidden

def roles_required(*user_types):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.user_type in user_types:
                    return view_func(request, *args, **kwargs)
            elif 'anonymous' in user_types:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator
