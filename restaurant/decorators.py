from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.profile.role != "admin":
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper
