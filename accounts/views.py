from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignupForm


def register(request):
    """
        Display a registration form for a :model:`auth.User`.

        **Context**

        ``form``
            An instance of SignupForm

        **Template:**

            :template:`registration/register.html`
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})
