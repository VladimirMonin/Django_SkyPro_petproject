# Generated by Django 4.1.3 on 2022-12-31 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('hr', 'HR'), ('unk', 'Unknown'), ('emp', 'Employee')], default='unk', max_length=4),
        ),
    ]
