from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User

from core.models import CompanyProfile

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
		if email and User.objects.filter(email=email,username=email).count():
			raise forms.ValidationError('Email addresses must be unique.')
		return email

	class Meta:
		model = User
		# exclude = ('password2',)
		fields = ( 'first_name', 'last_name', 'email',)

  # def save(self, commit=True):
	 #  user = super(RegistrationFormBasic, self).save(commit=False)
	 #  # user.set_password(self.cleaned_data["password1"])
	 #  if commit:
	 #  	user.save()
	 #  return user

class RegistrationFormVerify(forms.Form):

	verify_code = forms.RegexField( regex=r'^[0-9]*$', widget=forms.TextInput(
		attrs={'required': True, 'max_length': 30, 'render_value': False,
             'placeholder': 'Enter verification code'} ), label=("Verification code"), error_messages={
		'invalid': ("This value must contain only letters")} )
		

class RegistrationFormPassword(forms.ModelForm):
  
	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'required': True, 'max_length': 30, 'render_value': False,
      'placeholder': 'Password'}),
      label=("Password"))
	class Meta:
		model = User
      # exclude = ('password2',)
		fields = ( 'password1',)

  # def save(self, commit=True):
	 #  user = super(RegistrationFormPassword, self).save(commit=False)
	 #  user.set_password(self.cleaned_data["password1"])
	 #  if commit:
	 #  	user.save()
	 #  return user

class SetupCompanyProfile(forms.Form):
  
	company_name = forms.RegexField( regex=r'^[A-Za-z ]*$', widget=forms.TextInput(
		attrs={'required': True, 'max_length': 30, 'render_value': False,
             'placeholder': 'Company  name'} ), label=("Company name"), error_messages={
      'invalid': ("This value must contain only letters")} )

	job_title = forms.RegexField( regex=r'^[A-Za-z ]*$', widget=forms.TextInput(
		attrs={'required': False, 'max_length': 30, 'render_value': False,
             'placeholder': 'Job Title'} ), label=("Job title"), error_messages={
      'invalid': ("This value must contain only letters")} )

	class Meta:
		model = CompanyProfile
      # exclude = ('password2',)
		fields = ( 'company_name', 'job_title', )


class SetupCompanyProfileFinal(forms.ModelForm):
  
	portal_url = forms.RegexField( regex=r'^[A-Za-z]*$', widget=forms.TextInput(
		attrs={'required': True, 'max_length': 30, 'render_value': False,
             'placeholder': 'Portal URL'} ), label=("Portal URL"), error_messages={
      'invalid': ("This value must contain only letters")} )

	def check_portal(self):
		portal_url = self.cleaned_data.get('portal_url')
		if portal_url and CompanyProfile.objects.filter(portal_url=portal_url).count():
		  raise forms.ValidationError('portal url must be unique.')
		return portal_url

	class Meta:
		model = CompanyProfile
      # exclude = ('password2',)
		fields = ( 'portal_url', 'logo', )

class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(
		attrs={ 'max_length': '30', 'required': True,
               'placeholder': 'Email'}), label=("Email"))
	password = forms.CharField(
		widget=forms.PasswordInput(
            attrs={'max_length': '30', 'required': True,
                   'placeholder': 'Password'}), label=("Password"))

	class Meta:
		model = User
		fields = ( 'email', 'password',)