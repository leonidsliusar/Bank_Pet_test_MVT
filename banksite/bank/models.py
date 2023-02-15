from django.db import models
from phone_field import PhoneField

class Account(models.Model):
    login = models.CharField(verbose_name="login", max_length=55)
    password = models.CharField(verbose_name='password', max_length=55)
    first_name = models.CharField(verbose_name="name", max_length=55)
    last_name = models.CharField(verbose_name="surename", max_length=55, db_index=True)
    middle_name = models.CharField(verbose_name="otchestvo", max_length=55, blank=True, default=None)
    birth_date = models.DateField(verbose_name="birth")
    registation_date = models.DateTimeField(auto_created=True, auto_now_add=True)
    email = models.EmailField(verbose_name="email", unique=True)
    phone = models.CharField(max_length=13, unique=True)
    avatar = models.ImageField(verbose_name="avatar")

    def __str__(self):
        return "id" + str(self.pk) + " " + self.first_name + " " + self.last_name

class Wallet(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="wallet")
    balance = models.DecimalField(verbose_name="balance", max_digits=20, decimal_places=2, default=0)
    wallet_id = models.CharField(max_length=12, default=None, unique=True, blank=True)