# Generated by Django 5.2.1 on 2025-06-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responses', '0005_alter_questionnaireresponse_role_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaireresponse',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
