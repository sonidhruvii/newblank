# Generated by Django 5.1.7 on 2025-03-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='logintable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email_id', models.EmailField(max_length=254)),
                ('phone_no', models.BigIntegerField()),
                ('password', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('status', models.CharField(max_length=20)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
