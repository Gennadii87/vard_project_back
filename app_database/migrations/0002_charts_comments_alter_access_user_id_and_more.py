# Generated by Django 4.0 on 2024-03-18 07:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_change', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.userproxy')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_send', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_remove', models.DateTimeField(blank=True, null=True)),
                ('data_delivery', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('chart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.charts')),
            ],
        ),
        migrations.AlterField(
            model_name='access',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.userproxy'),
        ),
        migrations.AlterField(
            model_name='files',
            name='data_change',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='files',
            name='data_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ReadComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_reading', models.DateTimeField(auto_now_add=True)),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.comments')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.userproxy')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('theme', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.userproxy')),
            ],
        ),
        migrations.CreateModel(
            name='Dashboards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_change', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.userproxy')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='file_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.files'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_database.userproxy'),
        ),
    ]
