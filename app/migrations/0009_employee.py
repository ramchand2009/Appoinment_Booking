# Generated by Django 3.2.20 on 2023-07-28 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_customer_customer_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer_name', models.CharField(max_length=250)),
                ('Customer_mobile', models.CharField(blank=True, max_length=10, null=True)),
                ('Customer_email', models.EmailField(max_length=254)),
                ('Customer_Address', models.CharField(max_length=250)),
                ('Customer_Status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employee',
            },
        ),
    ]
