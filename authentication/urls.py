from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserCreateView, UserLogout

urlpatterns = [
    path('create/', UserCreateView.as_view()),
    path('login/', views.obtain_auth_token),  # вьюшка которая нам даст auth_token (написана функцией)
    path('logout/', UserLogout.as_view()),
    path('token/', TokenObtainPairView.as_view()),  # Получение пары JWT токенов по паролю
    path('token/refresh/', TokenRefreshView.as_view()),  # Получение access токена по refresh токену

]
