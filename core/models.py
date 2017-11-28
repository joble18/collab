from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CompanyProfile(models.Model):
   
    timezone = models.CharField(max_length=80)
    company_name = 	models.CharField(max_length=80)
    job_title = models.CharField(max_length=80)
    portal_url = models.CharField(max_length=80, unique=True)
    logo = models.ImageField(upload_to = 'logo/',null=True,
                        blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)