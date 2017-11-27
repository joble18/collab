# from django.shortcuts import render
# from django.http import HttpResponse
import pytz
from random import randint
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, TemplateView, FormView

from core.forms import RegistrationFormBasic, RegistrationFormVerify, RegistrationFormPassword, SetupCompanyProfile


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
        self.request.session['otp'] = randint(100, 999)
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
        # form.set_password(self.cleaned_data["password1"])
        user_object = form.save(commit=False)
        user_object.username = self.request.session['email']
        user_object.email = self.request.session['email']
        user_object.first_name = self.request.session['first_name']
        user_object.last_name = self.request.session['last_name']
        # user_object.is_active = False
        user_object.save()
        # form.username = self.request.session['user']
        # form.first_name = self.request.session['first_name']
        # form.last_name = self.request.session['last_name']
        # form.save()
        return HttpResponseRedirect(reverse_lazy("setupcompanyprofile"))

class SetupCompanyProfile(FormView):
        
    form_class = SetupCompanyProfile
    template_name = 'setup_company.html'
    # success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SetupCompanyProfile, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['timezones'] = pytz.common_timezones
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy("setupcompanyprofile"))