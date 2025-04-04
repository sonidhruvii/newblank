# Generated by Django 5.1.7 on 2025-03-31 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_category_login_delete_logintable'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ITEM_NAME', models.CharField(max_length=30)),
                ('ITEM_PRICE', models.IntegerField()),
                ('ITEM_DESC', models.TextField()),
                ('ITEM_IMG', models.ImageField(upload_to='photos')),
                ('CAT_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.category', verbose_name='CAT_ID')),
                ('SELLER_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.login')),
            ],
        ),
    ]
