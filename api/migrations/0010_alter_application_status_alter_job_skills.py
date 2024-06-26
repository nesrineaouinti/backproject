# Generated by Django 5.0.5 on 2024-05-13 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_job_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('sent', 'Sent'), ('in review', 'In review'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='sent', max_length=10),
        ),
        migrations.AlterField(
            model_name='job',
            name='skills',
            field=models.CharField(default='no_skills', max_length=500),
        ),
    ]
