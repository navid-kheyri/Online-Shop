from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import  get_object_or_404
from vendors.models import Vendor
from website.models import Product

def roles_required(*user_types,pk_is_user=False,pk_is_vednor=False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.user_type in user_types :

                    if pk_is_user and int(kwargs.get('pk')) == request.user.pk :
                        return view_func(request, *args, **kwargs)
                    
                    elif pk_is_vednor :
                        vendor = get_object_or_404(Vendor,pk=kwargs.get('pk'))
                        if vendor.user_has_permission(request.user):
                            return view_func(request, *args, **kwargs)
                        
                    elif not pk_is_user and not pk_is_vednor in user_types:
                        return view_func(request, *args, **kwargs)
                    
                    return HttpResponseForbidden("You do not have permission to access this page.")
            elif 'anonymous' in user_types:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapped_view
    return decorator