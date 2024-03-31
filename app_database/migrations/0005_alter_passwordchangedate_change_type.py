# Generated by Django 4.0 on 2024-03-31 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_database', '0004_alter_file_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordchangedate',
            name='change_type',
            field=models.CharField(choices=[('created', 'Пароль создан'), ('changed', 'Пароль изменен')], default='changed', editable=False, max_length=10),
        ),
    ]
