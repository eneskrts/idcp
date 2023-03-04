# Generated by Django 4.1.3 on 2023-03-03 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_profile_phone_alter_employee_currency_unit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyUnitNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TitleNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('label', models.CharField(max_length=200)),
            ],
        ),
    ]
