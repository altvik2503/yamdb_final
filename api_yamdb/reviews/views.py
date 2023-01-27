from django.shortcuts import redirect


def default_redirect(request):
    """View-функция url ''."""
    return redirect(to='/admin')
