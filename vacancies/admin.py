from django.contrib import admin

from vacancies.models import Vacancy, Skill

admin.site.register(Vacancy)  # Минимально достаточно чтобы запустить админку. Если нужна кастомизация - надо будет писать админ класс
admin.site.register(Skill)
