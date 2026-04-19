# home/decorators.py
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            role = request.session.get('user_role')

            if role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # If doctor tries to access other views
            if role == 'doctor':
                return redirect('patient_dashboard')
            elif role == 'admin':
                return redirect('analytics_dashboard')
            else:
                return redirect('signin')
        return _wrapped_view
    return decorator
