# Generated by Django 4.0 on 2024-04-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mybase', '0004_rename_database_host_userdatabaseprofile_db_host_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatabaseprofile',
            name='name_profile',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
