# Generated by Django 4.1.7 on 2023-02-20 17:59

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bank', '0002_remove_wallet_account_delete_account_delete_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registation_date', models.DateTimeField(auto_created=True)),
                ('login', models.CharField(max_length=55, verbose_name='login')),
                ('password', models.CharField(max_length=55, verbose_name='password')),
                ('first_name', models.CharField(max_length=55, verbose_name='name')),
                ('last_name', models.CharField(db_index=True, max_length=55, verbose_name='surename')),
                ('middle_name', models.CharField(blank=True, default=None, max_length=55, verbose_name='otchestvo')),
                ('birth_date', models.DateField(verbose_name='birth')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('phone', phone_field.models.PhoneField(blank=True, max_length=13, unique=True)),
                ('avatar', models.ImageField(upload_to='', verbose_name='avatar')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='balance')),
                ('wallet_id', models.CharField(blank=True, default=None, max_length=12, unique=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.account', verbose_name='wallet')),
            ],
        ),
    ]