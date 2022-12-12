import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from vacancies.models import Vacancy, Skill


def hello(request):
    return HttpResponse('Это pet prodject для изучения Django в SkyPro')


@method_decorator(csrf_exempt, name='dispatch')  # Таким образом мы можем обвернуть целый класс в декоратор csrf_exempt
class VacancyListView(ListView):
    model = Vacancy  # Указываем модель с которой будем работать

    def get(self, request, *args,
            **kwargs):  # request - все данные полученные от пользователя и собранные в красивый класс
        super().get(request, *args, **kwargs)  # После этого появится objects.list self

        search_text = request.GET.get('text', None)  # Чтобы вернул None если
        # request не содержит ключа text
        if search_text:
            vacancies = self.object_list.filter(text=search_text)  # производим поиск по БД
        response = []
        for vacancy in self.object_list:
            response.append(
                {
                    'id': vacancy.id,
                    'text': vacancy.text,
                    'slug': vacancy.slug,
                    'status': vacancy.status,
                    'created': vacancy.created,
                    'user': vacancy.user
                }
            )
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
                'user': vacancy.user
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
                'user': vacancy.user

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
                'user': self.object.user

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
