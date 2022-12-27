from random import choices

from django.contrib.auth.models import User
from django.db import models


class Prifile(models.Model): # Создали доп. таблицу. Ссылкается на пользователя. На 1 запись пользователя - 1 профиль
    MALE = 'm'
    FEMALE = 'f'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
