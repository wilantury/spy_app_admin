# Generated by Django 3.2.6 on 2021-08-25 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spy',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]