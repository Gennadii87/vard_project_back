# Generated by Django 4.0 on 2024-04-02 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mybase', '0002_alter_userdatabaseprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatabaseprofile',
            name='database_type',
            field=models.CharField(choices=[('mysql', 'MySQL'), ('postgresql', 'PostgreSQL')], default='mysql', max_length=10),
        ),
    ]
