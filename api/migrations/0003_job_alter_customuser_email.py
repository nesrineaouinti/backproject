# Generated by Django 5.0.5 on 2024-05-10 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_customuser_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('summary', models.TextField()),
                ('salary', models.IntegerField(default=0)),
                ('skills', models.CharField(max_length=500)),
                ('promoted', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=254, unique=True),
        ),
    ]
