# Generated by Django 4.0.1 on 2022-01-26 14:28

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(default='news/default.jpg', upload_to=core.models.upload_to, verbose_name='Image'),
        ),
    ]
