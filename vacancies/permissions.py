from rest_framework.permissions import BasePermission

from authentication.models import User


class VacancyCreatePermission(BasePermission):
    message = 'Добавление вакансий разрешено только для HR!'

    def has_permission(self, request, view):
        return request.user.role == User.HR
