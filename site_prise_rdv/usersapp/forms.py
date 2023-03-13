from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
	first_name = forms.CharField(label='Prénom')
	last_name = forms.CharField(label='Nom')
	email = forms.EmailField(label='Adresse e-mail')
	
class Meta(UserCreationForm.Meta):
	model = User
	fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email')
 
class UserProfileForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Old password is incorrect')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user

