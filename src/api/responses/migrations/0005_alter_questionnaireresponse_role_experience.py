# Generated by Django 5.2.1 on 2025-06-01 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responses', '0004_questionnaireresponse_role_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaireresponse',
            name='role_experience',
            field=models.CharField(choices=[('<1', 'Junior'), ('1-3', 'Semi Senior'), ('>5', 'Senior')], default='<1', max_length=4),
        ),
    ]
