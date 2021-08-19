from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class BackTest(models.Model):
    symbol = models.CharField(max_length=200)
    Quantity = models.IntegerField()
    # Initial_Capital = models.IntegerField()
    Time_frame = models.CharField(max_length=200)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.to_date = timezone.now()
        self.from_date = timezone.now()
        self.save()


class ProfileDB(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=25, primary_key=True)
    phonenumber = PhoneNumberField(null=False, blank=True, unique=True)
    country = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    description = models.CharField(max_length=100, blank=True)
