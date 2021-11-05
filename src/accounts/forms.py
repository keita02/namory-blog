from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# FORMULAIRE DE CONNECTION
class LoginForm(AuthenticationForm):
	username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Nom d'utilisateur"}))
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Mot de passe"}))


# FORMULAIRE D'INSCRIPTION
class RegisterUserForm(UserCreationForm):
	username  = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Nom d'utilisateur"}))
	email     = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':"Adresse Email"}))
	password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Mot de passe"}))
	password2 = forms.CharField(label="Confirmer mot de passe", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Confirmer votre mot de passe"}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')