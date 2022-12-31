from random import choices

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # Наследуемся от абстракции у которой нет таблицы (как у User) - значит будет создана
    # чистая таблица, не будет лишних запросов в базу и не надо помнить про связку один к одному
    MALE = 'm'
    FEMALE = 'f'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]

    HR = 'hr'
    EMPLOYEE = 'emp'
    UNKNOWN = 'unk'
    ROLE = [(HR, 'HR'), (UNKNOWN, 'Unknown'), (EMPLOYEE, 'Employee')]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    role = models.CharField(max_length=4, choices=ROLE, default=UNKNOWN)
