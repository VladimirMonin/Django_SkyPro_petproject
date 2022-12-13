from django.http import request, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from companies.models import Company


@method_decorator(csrf_exempt, name='dispatch')
class CompanyImageView(UpdateView):
    model = Company
    fields = ['name', 'logo']

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.logo = request.FILES['logo']   # FILES лежат все файлы которые послал пользователь
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'logo': self.object.logo.url if self.object.logo else None,  # Чтобы не было проблем с отображением - показываем урл - если его нет поставим NONE
        })
