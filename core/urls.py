from django.conf.urls import url
from django.views.generic import TemplateView

from . import views as accounts_view

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^login/$', accounts_view.LoginUserView.as_view(), name='login'),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name="home_login.html"), name='home_login'),
    url(r'^signup/$', accounts_view.SignUpViewBasic.as_view(), name='signup'),
    url(r'^signup/verify/$', accounts_view.SignUpViewVerify.as_view(), name='verifyemail'),
    url(r'^signup/setpassword/$', accounts_view.SignUpViewPassword.as_view(), name='setpassword'),
    url(r'^signup/companyprofile/$', accounts_view.SetupCompanyProfileView.as_view(), name='setupcompanyprofile'),
    url(r'^signup/companyprofile/final/$', accounts_view.SetupCompanyProfileFinalView.as_view(), name='setupcompanyprofile_final'),
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

]
