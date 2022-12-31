import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Django_Skypro_petprodject import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancySerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


def hello(request):
    return HttpResponse('Это pet prodject для изучения Django в SkyPro')


class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()  # это вместо указания модели
    serializer_class = VacancySerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )  # ПОИСК ПО ВХОЖДЕНИЮ icontains - без учета регистра, contains с учетом

        # Делаем поиск по вхождению хотя бы одного навыка, а передаем список навыков в поисковый запрос
        skills = request.GET.getlist('skill', None)  # GET - словареподобная структура. И этим методом мы берем список
        skills_q = None

        for skill in skills:
            if skills_q is None:
                skills_q = Q(skills__name__icontains=skill)  # Специальный класс для сбора условий фильтрации
            else:
                skills_q |= Q(skills__name__icontains=skill)  # Его можно соединять при помощи логических конструкций
            #  Так делается любая логическая операция (кроме И - оно по умолчанию)
        if skills_q:
            self.queryset = self.queryset.filter(skills_q)

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):  # Специализированный класс для детального отображения любого элемента
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]  # Список с доступами - этот проверяет что есть доступ на эту страницу


class VacancyCreateView(CreateAPIView):  # Тут не нужен csrf_exempt - т.к. оно заточено под работу как API
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count('vacancy')).order_by(
            'id')  # Этот метод добавляет к нашей записи доп. колонку в которую ложет данные что он сделал - например это значение функции (посчтитать, макс или мин) далее я делаю группировку по возрастанию ID

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)  # Пагинатор встроен в Джанго.
        page_number = request.GET.get('page')  # Достаём номер страницы из запроса
        page_object = paginator.get_page(page_number)  # Передаем в пагинатор и получаем страницу

        users = []

        for user in page_object:
            users.append({
                'id': user.id,
                'user': user.username,
                'vacancies': user.vacancies  # Как раз из юзер квери сета - который мы посчитали в переменной user_qs
            })

        response = {
            'items': users,
            'num_pages': paginator.num_pages,  # Посчитаем сколько всего страниц у нас будет
            'total': paginator.count,  # Посчитаем сколько всего юзеров
            'avg': user_qs.aggregate(avg=Avg('vacancies'))['avg']
            # aggregate - терминальная функция, после неё уже нельзя использовать гурппировки. Тут мы говорим сделай Avg, положи в ключ avg и последний список после скобок (чтобы было плоско)
        }

        return JsonResponse(response, safe=False, json_dumps_params={
            'ensure_ascii': False})


class VacancyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)  # Взяли модель вакансии,
        # Отфильтровали по первичным ключам. PK входит в список - а список берем из данных которые пришли. Сразу на
        # эту штуку применим update. Методы можно вешать до бесконечности или до первого терминального метода.
        # Обновляем поле likes. Делается это с помощью класса F - он говорит что это поле текущей записи. Возьми
        # текущее значение и сделай с ним всякое

        return JsonResponse(
            VacancyDetailSerializer(Vacancy.objects.filter(pk__in=request.data),
                                    many=True).data,
                                    safe=False,
        )
