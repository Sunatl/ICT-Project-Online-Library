from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from Menu.models import *
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'phone_number','email','grade']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
    
class Singup(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/singup.html" 