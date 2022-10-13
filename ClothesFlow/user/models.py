from django.db import models

from phone_field import PhoneField

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, blank=False)


INSTITUTION_CHOICES = (
    (1, 'FOUNDATION'),
    (2, 'NON-GOVERNMENTAL ORGANIZATION'),
    (3, 'LOCAL COLLECTION'),
)


class Institution(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True)
    description = models.TextField(blank=False)
    type = models.CharField(max_length=2, choices=INSTITUTION_CHOICES, default='FOUNDATION')
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128, default='ul.Długa 44/4')
    phone_number = PhoneField(blank=True, help_text = 'Contact Phone Number')
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField(null=False, blank=False, help_text='2022-12-12')
    pick_up_time = models.TimeField(null=False, blank=False, help_text='12:00')
    pick_up_comment = models.TextField(max_length=1024)
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)

