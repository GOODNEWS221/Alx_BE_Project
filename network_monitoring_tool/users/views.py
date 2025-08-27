from rest_framework import generics
from django.contrib.auth import get_user_model
from .models import Role
from .serializers import UserSerializer, RoleSerializer, RegisterSerializer
from .permissions import IsAdmin
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, RoleForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  # Anyone can register


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]


# --- Users ---
def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})

def user_add(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user-list")
    else:
        form = UserForm()
    return render(request, "users/user_form.html", {"form": form, "form_title": "Add User"})

def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-list")
    else:
        form = UserForm(instance=user)
    return render(request, "users/user_form.html", {"form": form, "form_title": "Edit User"})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("user-list")
    return render(request, "users/user_form.html", {"form": None, "form_title": "Delete User"})

def role_list(request):
    roles = Role.objects.all()
    return render(request, "users/role_list.html", {"roles": roles})

def role_add(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("role-list")
    else:
        form = RoleForm()
    return render(request, "users/role_form.html", {"form": form, "form_title": "Add Role"})

def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect("role-list")
    else:
        form = RoleForm(instance=role)
    return render(request, "users/role_form.html", {"form": form, "form_title": "Edit Role"})

def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        role.delete()
        return redirect("role-list")
    # You can show a simple confirmation page or reuse form
    return render(request, "users/role_form.html", {"form": None, "form_title": "Delete Role"})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    # your existing dashboard logic
    return render(request, 'dashboard.html')