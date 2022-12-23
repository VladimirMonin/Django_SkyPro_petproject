import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from Django_Skypro_petprodject import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancySerializer, VacancyDetailSerializer, VacancyCreateSerializer


def hello(request):
    return HttpResponse('Это pet prodject для изучения Django в SkyPro')


@method_decorator(csrf_exempt, name='dispatch')  # Таким образом мы можем обвернуть целый класс в декоратор csrf_exempt
class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()  # это вместо указания модели
    serializer_class = VacancySerializer


class VacancyDetailView(RetrieveAPIView):  # Специализированный класс для детального отображения любого элемента
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer



class VacancyCreateView(CreateAPIView):  # Тут не нужен csrf_exempt - т.к. оно заточено под работу как API
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    # model = Vacancy
    # fields = ['user', 'status', 'created', 'slug', 'skills',
    #           'text']  # Нужно для генерации формы. Её мы не будем использовать. Но т.к. это неотъемлимый атрибут джанго - приходится писать
    #
    # def post(self, request, *args, **kwargs):
    #     vacancy_data = VacancyCreateSerializer(data=json.loads(request.body)) # Из тела запроса в json - потом в объект Python
    #     if vacancy_data.is_valid():  # Проверяем что все данные в нужных форматах и подходят
    #         vacancy_data.save()  # Прямо из сериализатора сохраняем
    #
    #     else:
    #         return JsonResponse(vacancy_data.errors)
    #
    #     return JsonResponse(
    #         vacancy_data.data,
    #         safe=False, json_dumps_params={'ensure_ascii': False}
    #     )
    #

@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ['status', 'slug', 'skills',
              'text']  # Копия с CreateView, но тут мы не будем редактировать пользователя и дату создания

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(
            request.body)  # Вытаскиваем данные для сохранения из тела запроса POST и приводим в вид словаря для дальнейшей работы

        self.object.slug = vacancy_data['slug']
        self.object.status = vacancy_data['status']
        self.object.text = vacancy_data['text']

        for skill in vacancy_data['skills']:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({"error": "Skill not found"}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()  # Тут он не сохраняется автоматом - поэтому делаем это вручную

        return JsonResponse(
            {
                'id': self.object.id,
                'text': self.object.text,
                'slug': self.object.slug,
                'status': self.object.status,
                'created': self.object.created,
                'skills': list(self.object.skills.all().values_list("name", flat=True)),
                # это many to many поле которое ссылается на таблицу
                # с ключами, просто так не выведешь. Мы делаем запрос в БД. Без этого никак. Берем скиллы, достаем все
                # говорим что нам надо достать тоьлко имена (в плоском виде) и заворачиваем в список

            }
            , json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


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
