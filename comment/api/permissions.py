from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = 'You must be the owner of this object.' # objenin sahibi siz olmalısınız.

    def has_permission(self, request, view):   # burası her zaman çalışır.
        return request.user and request.user.is_authenticated  # giriş yapanlara izin verir.

    def has_object_permission(self, request, view, obj):        # değiştiren veya silen kişi bu yorumun sahibi mi?
        return obj.user == request.user    # işlem yapıldığı sırada kontrol sağlıyor.
