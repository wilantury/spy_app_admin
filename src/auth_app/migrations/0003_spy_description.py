# Generated by Django 3.2.6 on 2021-08-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_alter_spy_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='spy',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]