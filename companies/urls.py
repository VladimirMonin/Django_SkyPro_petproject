from django.contrib import admin
from django.urls import path

from companies import views

# В такой интерпретации urls (когда они лежат внутри каждого app - оставляем сам путь без префикса)
urlpatterns = [

    path('image/<int:pk>/', views.CompanyImageView.as_view()),
    # специальный метод as.view() делает вызываемым класс (с передачей реквеста внутрь и упрощая задачу)

]
