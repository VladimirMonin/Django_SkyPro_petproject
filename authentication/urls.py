from django.urls import path
from rest_framework.authtoken import views

from authentication.views import UserCreateView, UserLogout

urlpatterns = [
    path('create/', UserCreateView.as_view()),
    path('login/', views.obtain_auth_token),  # вьюшка которая нам даст auth_token (написана функцией)
    path('logout/', UserLogout.as_view()),

]
