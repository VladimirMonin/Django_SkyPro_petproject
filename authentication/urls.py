from django.urls import path

from authentication.views import UserCreateView

urlpatterns = [
    path('create/', UserCreateView.as_view()),

]
