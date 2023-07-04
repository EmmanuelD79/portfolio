from django.shortcuts import redirect

def guest_required(redirect_to):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if (request.user.is_superuser) or (not request.user.is_anonymous and request.user.is_guest and request.user.is_authenticated) :
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_to)
        return wrapper
    return decorator
