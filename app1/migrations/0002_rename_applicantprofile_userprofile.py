# Generated by Django 4.2.2 on 2023-06-12 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApplicantProfile',
            new_name='UserProfile',
        ),
    ]