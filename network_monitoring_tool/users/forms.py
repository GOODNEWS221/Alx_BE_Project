from django import forms
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# --- Roles ---
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name", "description"]
