import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


def hello(request):
    return HttpResponse('Это pet prodject для изучения Django в SkyPro', safe=False, json_dumps_params={
        'ensure_ascii': True
    })  # safe=False - если мы например хотим передать не словарь а список - говорим что не надо проверять подходит ли в Json


@method_decorator(csrf_exempt, name='dispatch')  # Таким образом мы можем обвернуть целый класс в декоратор csrf_exempt
class VacancyView(View):

    def get(self, request):  # request - все данные полученные от пользователя и собранные в красивый класс
        if request.method == 'GET':
            vacancies = Vacancy.objects.all()  # Формально objects это менеджер, но пока можно сказать это ORM - т.е. общение с БД

            # search_text = request.GET['text']  # Если был передан query параметр text для поиска
            search_text = request.GET.get('text', None)  # Чтобы вернул None если ничего не найдет
            if search_text:
                vacancies = vacancies.filter(text=search_text)  # производим поиск по БД
            response = []
            for vacancy in vacancies:
                response.append(
                    {
                        'id': vacancy.id,
                        'text': vacancy.text,
                        'slug': vacancy.slug,
                        'status': vacancy.status
                    }
                )
            return JsonResponse(response, safe=False, json_dumps_params={
                'ensure_ascii': False})  # Второй аргумент, там не словарь, но оно может быть Json третий - можно передать параметры дампа

    def post(self, request):
        vacansy_data = json.loads(
            request.body)  # Вытаскиваем данные для сохранения из тела запроса POST и приводим в вид словаря для дальнейшей работы
        vacancy = Vacancy()  # Создали объект класса модели
        vacancy.text = vacansy_data['text']
        vacancy.slug = vacansy_data['slug']
        vacancy.status = vacansy_data['status']

        vacancy.save()  # Сохраняем данные. Метод сейв вызовет запрос на INSERT в БД

        return JsonResponse(
            {
                'id': vacancy.id,
                'text': vacancy.text,
                'slug': vacancy.slug,
                'status': vacancy.status

            }
        )


class VacancyDetail(DetailView):  # Специализированный класс для детального отображения любого элемента
    model = Vacancy  # Обязательный атрибут клсса DetailView - модель которую он детализирует

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()  # Встроенный метод который вернет наш элемент

        return JsonResponse(
            {
                'id': vacancy.id,
                'text': vacancy.text,
                'slug': vacancy.slug,
                'status': vacancy.status
            }
            , safe=False, json_dumps_params={'ensure_ascii': False})
