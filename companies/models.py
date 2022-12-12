from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='logos/')  # Путь относительно Альбина как воды в рот набрала. 2-10 - чего???
