
from django.contrib import admin
from django.urls import path

from vacancies import views
# В такой интерпретации urls (когда они лежат внутри каждого app - оставляем сам путь без префикса)
urlpatterns = [

    path('list/', views.VacancyListView.as_view()),  # специальный метод as.view() делает вызываемым класс (с передачей реквеста внутрь и упрощая задачу)
    path('detail/<int:pk>/', views.VacancyDetailView.as_view()),  # тут передается либо pk либо slug
    path('create/', views.VacancyCreateView.as_view()),
    path('update/<int:pk>/', views.VacancyUpdateView.as_view()),
    path('by_users/', views.UserVacancyDetailView.as_view()),
    path('delete/<int:pk>/', views.VacancyDeleteView.as_view())

]
