from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)
