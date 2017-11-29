# from django.shortcuts import render
# from django.http import HttpResponse
import pytz
from random import randint
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, CreateView, TemplateView, FormView
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.models import User

from apps.core.forms import RegistrationFormBasic, RegistrationFormVerify, RegistrationFormPassword,SetupCompanyProfile, SetupCompanyProfileFinal, LoginForm


# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# def signup(request):
#     if request.method == 'POST':
#         import pdb; pdb.set_trace()
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             print(24242)
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#         # print(form.errors)
#     return render(request, 'signup.html', {'form': form})

# def home(request):
#     return render(request, 'home.html', {})

class SignUpViewBasic(FormView):
    """docstring for SignUpView"""
    # def __init__(self, arg):
    #     super(SignUpView, self).__init__()
    #     self.arg = arg
        
    form_class = RegistrationFormBasic
    template_name = 'signup_basic.html'
    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        # user_object = form.save()
        # user_object.username = form.cleaned_data['email']
        self.request.session['email'] = form.cleaned_data['email']
        self.request.session['first_name'] = form.cleaned_data['first_name']
        self.request.session['last_name'] = form.cleaned_data['last_name']
        # user_object.save()
        body = randint(100, 999)
        self.request.session['otp'] = body
        email = EmailMessage('Activate Your Account', "Your verification code is: "+str(body), settings.DEFAULT_FROM_EMAIL, (form.cleaned_data['email'],))
        email.content_subtype = 'html'

        try:
            email.send()
        except Exception as e:
            print(e)
        print('>>>>>>>>>>>>OTP' + str(self.request.session['otp']))
        return HttpResponseRedirect(reverse_lazy("verifyemail"))
        # pass

class SignUpViewVerify(FormView):
    """docstring for SignUpView"""
    # def __init__(self, arg):
    #     super(SignUpView, self).__init__()
    #     self.arg = arg
        
    form_class = RegistrationFormVerify
    template_name = 'signup_verify.html'
    # success_url = reverse_lazy("home")


    def form_valid(self, form):
        # form.save()
        if self.request.session['otp'] == int(form.cleaned_data['verify_code']):

            return HttpResponseRedirect(reverse_lazy("setpassword"))
        else:
            return HttpResponseRedirect(reverse_lazy("verifyemail"))

class SignUpViewPassword(CreateView):
        
    form_class = RegistrationFormPassword
    template_name = 'signup_password.html'
    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        # form.save(commit=False)
        # form.set_password(setpasswordlf.cleaned_data["password1"])

        user_object = form.save(commit=False)
        user_object.set_password(self.request.POST.get("password1"))
        user_object.username = self.request.session['email']
        user_object.email = self.request.session['email']
        user_object.first_name = self.request.session['first_name']
        user_object.last_name = self.request.session['last_name']
        user_object.save()
        self.request.session['current_user'] = user_object.id
        
     
        # form.username = self.request.session['user']
        # form.first_name = self.request.session['first_name']
        # form.last_name = self.request.session['last_name']
        # form.save()
        return HttpResponseRedirect(reverse_lazy("setupcompanyprofile"))

class SetupCompanyProfileView(FormView):
        
    form_class = SetupCompanyProfile
    template_name = 'setup_company.html'
    # success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SetupCompanyProfileView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['timezones'] = pytz.common_timezones
        return context

    def form_valid(self, form):
        # company_object = form.save(commit=False)
        # print(form)
        self.request.session['company_name'] = form.cleaned_data['company_name']
        self.request.session['timezone'] = self.request.POST.get('timezone')
        self.request.session['job_title'] = form.cleaned_data['job_title']

        return HttpResponseRedirect(reverse_lazy("setupcompanyprofile_final"))

class SetupCompanyProfileFinalView(FormView):
        
    form_class = SetupCompanyProfileFinal
    template_name = 'setup_company_final.html'
    owner = None
    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        # company_object = form.save(commit=False)

        
        company_object = form.save(commit=False)
        company_object.portal_url = form.cleaned_data.get('portal_url')
        company_object.timezone = self.request.session.get('timezone')
        company_object.company_name = self.request.session.get('company_name')
        company_object.job_title = self.request.session.get('job_title')
        company_object.logo =form.cleaned_data.get('logo')
        try:
            self.owner = User.objects.get(id=self.request.session.get('current_user')) 
        except User.DoesNotExist:
            self.owner = None
        company_object.owner = self.owner
        company_object.save()
        return HttpResponse('Account Created')

    def form_invalid(self, form):
        print(form.errors)

class LoginUserView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy("home")