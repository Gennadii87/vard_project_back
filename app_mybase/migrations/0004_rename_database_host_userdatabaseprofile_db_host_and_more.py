# Generated by Django 4.0 on 2024-04-02 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_mybase', '0003_userdatabaseprofile_database_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdatabaseprofile',
            old_name='database_host',
            new_name='db_host',
        ),
        migrations.RenameField(
            model_name='userdatabaseprofile',
            old_name='database_password',
            new_name='db_password',
        ),
        migrations.RenameField(
            model_name='userdatabaseprofile',
            old_name='database_port',
            new_name='db_port',
        ),
        migrations.RenameField(
            model_name='userdatabaseprofile',
            old_name='database_type',
            new_name='db_type',
        ),
        migrations.RenameField(
            model_name='userdatabaseprofile',
            old_name='database_username',
            new_name='db_username',
        ),
    ]
