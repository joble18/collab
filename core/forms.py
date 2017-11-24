from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User

class RegistrationFormBasic(forms.ModelForm):
  first_name = forms.RegexField( regex=r'^[A-Za-z]*$', widget=forms.TextInput(
      attrs={'required': True, 'max_length': 30, 'render_value': False,
             'placeholder': 'First Name'} ), label=("First Name"), error_messages={
      'invalid': ("This value must contain only letters")} )
  
  last_name = forms.RegexField( regex=r'^[A-Za-z]*$', widget=forms.TextInput(
      attrs={'required': True, 'max_length': 30, 'render_value': False,
             'placeholder': 'Last Name'} ), label=("Last Name"), error_messages={
      'invalid': ("This value must contain only letters")} )
  
  email = forms.EmailField(widget=forms.TextInput(
      attrs={'required': True, 'max_length': 30, 'render_value': False,
             'unique': True, 'placeholder': 'Email address'}),
      label=("Email address"))
  
  # password2 = forms.CharField(
  #     widget=forms.PasswordInput(attrs={'required': True, 'max_length': 30, 'render_value': False,
  #                                        'placeholder': 'Confirm Password'}),
  #     label=("Confirm Password"))

  def clean_email(self):
      email = self.cleaned_data.get('email')
      if email and User.objects.filter(email=email).count():
          raise forms.ValidationError('Email addresses must be unique.')
      return email

  class Meta:
      model = User
      # exclude = ('password2',)
      fields = ( 'first_name', 'last_name', 'email',)

  def save(self, commit=True):
	  user = super(RegistrationForm, self).save(commit=False)
	  user.set_password(self.cleaned_data["password1"])
	  if commit:
	  	user.save()
	  return user

class RegistrationFormVerify(forms.Form):

	verify_code = forms.RegexField( regex=r'^[A-Za-z]*$', widget=forms.TextInput(
      attrs={'required': True, 'max_length': 30, 'render_value': False,
             'placeholder': 'Enter verification code'} ), label=("Verification code"), error_messages={
      'invalid': ("This value must contain only letters")} )
		

class RegistrationFormPassword(forms.Form):
  
	password1 = forms.CharField(
      widget=forms.PasswordInput(attrs={'required': True, 'max_length': 30, 'render_value': False,
      'placeholder': 'Password'}),
      label=("Password"))