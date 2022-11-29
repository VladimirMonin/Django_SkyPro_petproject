from django.db import models


class Vacancy(models.Model):
    text = models.CharField(max_length=2000)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.text
