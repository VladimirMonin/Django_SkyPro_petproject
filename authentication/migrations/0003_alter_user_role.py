# Generated by Django 4.1.3 on 2023-01-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('hr', 'hr'), ('unk', 'unk'), ('emp', 'emp')], default='unk', max_length=4),
        ),
    ]
