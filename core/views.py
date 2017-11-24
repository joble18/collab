# from django.shortcuts import render
# from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, TemplateView, FormView

from core.forms import RegistrationFormBasic, RegistrationFormVerify


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

class SignUpViewBasic(View):
    """docstring for SignUpView"""
    # def __init__(self, arg):
    #     super(SignUpView, self).__init__()
    #     self.arg = arg
        
    form_class = RegistrationFormBasic
    template_name = 'signup_basic.html'
    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        user_object = form.save()
        user_object.username = form.cleaned_data['email']
        user_object.save()
        return HttpResponseRedirect(reverse_lazy("home"))
        # pass

class SignUpViewVerify(View):
    """docstring for SignUpView"""
    # def __init__(self, arg):
    #     super(SignUpView, self).__init__()
    #     self.arg = arg
        
    form_class = RegistrationFormVerify
    template_name = 'signup_verify.html'
    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy("home"))