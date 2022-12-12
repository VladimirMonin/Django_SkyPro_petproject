from django.contrib import admin
from django.urls import path, include

from vacancies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),  # comments: Показали что будет работать по этому адресу
    path('vacancy/', include('vacancies.urls')),  # добавили урлы из app vacancies
]
