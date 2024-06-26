# Generated by Django 5.0.5 on 2024-05-19 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_application_status_alter_job_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
