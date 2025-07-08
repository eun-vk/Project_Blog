from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # 이메일 필드 제외


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'profile_image']
        widgets = {
            'nickname': forms.TextInput(attrs={'placeholder': '닉네임'}),
            'bio': forms.Textarea(attrs={'placeholder': '소개'}),
        }

