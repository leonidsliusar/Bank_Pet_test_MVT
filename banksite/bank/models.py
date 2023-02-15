from django.db import models


class Account(models.Model):
    first_name = models.CharField(verbose_name="name", max_length=55)
    last_name = models.CharField(verbose_name="surename", max_length=55, db_index=True)
    middle_name = models.CharField(verbose_name="otchestvo", max_length=55, blank=True, default=None)
    birth_date = models.DateField(verbose_name="birth", auto_now=False)
    registation_date = models.DateTimeField(auto_created=True)
    email = models.EmailField(verbose_name="email", unique=True)
    avatar = models.ImageField(verbose_name="avatar")


class Wallet(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="wallet")
    balance = models.DecimalField(verbose_name="balance", max_digits=20, decimal_places=2, default=0)
    wallet_id = models.CharField(max_length=12, default=None, unique=True, blank=True)
