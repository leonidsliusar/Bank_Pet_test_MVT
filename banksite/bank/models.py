from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    middle_name = models.CharField(verbose_name="otchestvo", max_length=55, blank=True, default=None)
    birth_date = models.DateField(verbose_name="birth")
    phone = models.CharField(max_length=13, unique=True)
    avatar = models.ImageField(verbose_name="avatar")
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='0')
    def __str__(self):
        return "id" + str(self.pk) + " " + self.first_name + " " + self.last_name

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="wallet", default='0')
    balance = models.DecimalField(verbose_name="balance", max_digits=20, decimal_places=2, default=0)
    wallet_id = models.CharField(max_length=12, default=None, unique=True, blank=True)