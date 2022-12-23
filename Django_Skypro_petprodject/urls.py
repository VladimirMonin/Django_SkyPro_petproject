from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from vacancies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),  # Добавили урл из DRF - для проверки. В нём есть собственный urls.py - и пути для авторизации
    path('hello/', views.hello),  # comments: Показали что будет работать по этому адресу
    path('vacancy/', include('vacancies.urls')),  # добавили урлы из app vacancies
    path('company/', include('companies.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # добавили сам урл (с константы настроек а потом адрес папки тоже константой) работает только в режиме разработчика и для этого нужна проверка
