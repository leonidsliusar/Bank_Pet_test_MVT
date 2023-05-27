# Generated by Django 4.1.7 on 2023-05-27 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('bank', '0002_remove_wallet_account_delete_account_delete_wallet'), ('bank', '0003_initial'), ('bank', '0004_alter_account_registation_date'), ('bank', '0005_alter_account_phone'), ('bank', '0006_remove_account_email_remove_account_first_name_and_more'), ('bank', '0007_remove_wallet_account_wallet_user'), ('bank', '0008_remove_account_avatar')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='account',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middle_name', models.CharField(blank=True, default=None, max_length=55, verbose_name='otchestvo')),
                ('birth_date', models.DateField(verbose_name='birth')),
                ('phone', models.CharField(max_length=13, unique=True)),
                ('user', models.OneToOneField(default='0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='balance')),
                ('wallet_id', models.CharField(blank=True, default=None, max_length=12, unique=True)),
                ('user', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='wallet')),
            ],
        ),
    ]
