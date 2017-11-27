from django.db import models

# Create your models here.


class CompanyProfile(models.Model):
   
    timezone = models.CharField(max_length=80)
    company_name = 	models.CharField(max_length=80)
    job_title = models.CharField(max_length=80)
    portal_url = models.CharField(max_length=80)
    logo = models.CharField(max_length=80)