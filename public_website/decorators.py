from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


def belongs_to_group(group_name):
    return lambda user: user.groups.filter(name=group_name).exists()


def user_passes_test_message(test_func, message: str, redirect_to: str):
    """
    Decorator for views that checks that the user passes the given test,
    setting a message in case of no success. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.error(request, message)
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def login_required_message():
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

    actual_decorator = user_passes_test_message(
        lambda user: user.is_authenticated,
        message="Vous devez être connecté·e pour accéder à cette page",
        redirect_to=settings.LOGIN_URL,
    )
    return actual_decorator


def authorization_required_message(group_name: str):
    actual_decorator = user_passes_test_message(
        belongs_to_group(group_name),
        message="Vous êtes bien connecté·e, mais vous n'avez pas les droits pour accéder à cette page.",
        redirect_to="/services",
    )

    return actual_decorator
