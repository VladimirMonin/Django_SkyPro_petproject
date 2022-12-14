import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from Django_Skypro_petprodject import settings
from vacancies.models import Vacancy, Skill


def hello(request):
    return HttpResponse('Это pet prodject для изучения Django в SkyPro')


@method_decorator(csrf_exempt, name='dispatch')  # Таким образом мы можем обвернуть целый класс в декоратор csrf_exempt
class VacancyListView(ListView):
    model = Vacancy  # Указываем модель с которой будем работать

    def get(self, request, *args,
            **kwargs):  # request - все данные полученные от пользователя и собранные в красивый класс
        super().get(request, *args, **kwargs)  # После этого появится self.object_list

        self.object_list = self.object_list.order_by('id') # Делаем сортировку по ID

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)  # Пагинатор встроен в Джанго.
        page_number = request.GET.get('page')  # Достаём номер страницы из запроса
        page_object = paginator.get_page(page_number)  # Передаем в пагинатор и получаем страницу

        vacancies = []
        for vacancy in page_object:
            vacancies.append(
                {
                    'id': vacancy.id,
                    'text': vacancy.text,
                    'slug': vacancy.slug,
                    'status': vacancy.status,
                    'created': vacancy.created,
                    'skills': list(vacancy.skills.all().values_list("name", flat=True)),
                }
            )

        response = {  # Чтобы наш фронт мог отобразить всю пагинанацию
            'items': vacancies,  # Вакансии на странице
            'num_pages': paginator.num_pages,  # Посчитаем сколько всего страниц
            'total': paginator.count  # Посчитаем сколько всего запписей
        }
        return JsonResponse(response, safe=False, json_dumps_params={
            'ensure_ascii': False})  # Второй аргумент, там не словарь, но оно может быть Json третий - можно передать параметры дампа


class VacancyDetailView(DetailView):  # Специализированный класс для детального отображения любого элемента
    model = Vacancy  # Обязательный атрибут класса DetailView - модель которую он детализирует

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()  # Встроенный метод который вернет наш элемент

        return JsonResponse(
            {
                'id': vacancy.id,
                'text': vacancy.text,
                'slug': vacancy.slug,
                'status': vacancy.status,
                'created': vacancy.created,
                'skills': list(vacancy.skills.all().values_list("name", flat=True)),
            }
            , safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ['user', 'status', 'created', 'slug', 'skills',
              'text']  # Нужно для генерации формы. Её мы не будем использовать. Но т.к. это неотъемлимый атрибут джанго - приходится писать

    def post(self, request, *args, **kwargs):
        vacansy_data = json.loads(
            request.body)  # Вытаскиваем данные для сохранения из тела запроса POST и приводим в вид словаря для дальнейшей работы
        vacancy = Vacancy.objects.create(  # Вызывает save автоматически
            text=vacansy_data['text'],
            slug=vacansy_data['slug'],
            status=vacansy_data['status'],
            # id=vacansy_data['user_id'],

        )

        return JsonResponse(
            {
                'id': vacancy.id,
                'text': vacancy.text,
                'slug': vacancy.slug,
                'status': vacancy.status,
                'created': vacancy.created,
                'skills': list(vacancy.skills.all().values_list("name", flat=True)),

            }
            , safe=False, json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ['status', 'slug', 'skills',
              'text']  # Копия с CreateView, но тут мы не будем редактировать пользователя и дату создания

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacansy_data = json.loads(
            request.body)  # Вытаскиваем данные для сохранения из тела запроса POST и приводим в вид словаря для дальнейшей работы

        self.object.slug = vacansy_data['slug']
        self.object.status = vacansy_data['status']
        self.object.text = vacansy_data['text']

        for skill in vacansy_data['skills']:
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
                'skills': list(self.object.skills.all().values_list("name", flat=True)),  # это many to many поле которое ссылается на таблицу
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
        user_qs = User.objects.annotate(vacancies=Count('vacancy')) # Этот метод добавляет к нашей записи доп. колонку в которую ложет данные что он сделал - например это значение функции (посчтитать, макс или мин)

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
            'num_pages': paginator.num_pages,  # Посчитаем сколько всего страниц
            'total': paginator.count  # Посчитаем сколько всего записей
        }

        return JsonResponse(response, safe=False, json_dumps_params={
            'ensure_ascii': False})
