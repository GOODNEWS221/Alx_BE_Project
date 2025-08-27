from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # Optional: only logged-in users can see the dashboard
def dashboard(request):
    return render(request, "dashboard.html")

