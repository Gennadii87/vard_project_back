# Generated by Django 4.0 on 2024-04-01 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app_mybase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdatabaseprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
