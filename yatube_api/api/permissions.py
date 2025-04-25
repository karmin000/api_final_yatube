from rest_framework import permissions

class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Разрешает редактирование только автору объекта, остальным — только чтение."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author
