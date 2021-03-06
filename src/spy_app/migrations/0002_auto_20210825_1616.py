# Generated by Django 3.2.6 on 2021-08-25 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spy_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hit',
            name='is_taken',
        ),
        migrations.AddField(
            model_name='hit',
            name='assigment_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hit',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
