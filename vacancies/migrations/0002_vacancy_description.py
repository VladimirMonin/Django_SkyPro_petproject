# Generated by Django 4.1.3 on 2022-11-28 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='description',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
    ]
