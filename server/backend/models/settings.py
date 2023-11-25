from django.db import models


class Settings(models.Model):
    company_name = models.CharField(max_length=128, default='PeCoReT Project')
    company_street = models.CharField(max_length=255, default='Demo Street 5')
    company_city = models.CharField(max_length=255, default='Demo City')
    company_homepage = models.URLField(default='https://pecoret.github.io')
    company_email = models.EmailField(default='no-reply@pecoret.local')


    class Meta:
        ordering = ['pk']
