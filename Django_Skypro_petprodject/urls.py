
from django.contrib import admin
from django.urls import path

from vacancies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),  # comments: Показали что будет работать по этому адресу
    path('vacancy/', views.VacancyView.as_view()),  # специальный метод as.view() делает вызываемым класс (с передачей реквеста внутрь и упрощая задачу)
    path('vacancy/<int:pk>/', views.VacancyDetailView.as_view()),  # тут передается либо pk либо slug
    path('vacancy/create', views.VacancyCreateView.as_view()),
]