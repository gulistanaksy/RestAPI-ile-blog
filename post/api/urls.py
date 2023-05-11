from django.urls import path
from django.views.decorators.cache import cache_page

from post.api.views import PostListApiView, PostDetailAPIView, PostUpdateAPIView, PostCreateAPIView

app_name = "post"

urlpatterns = [
    path("list", cache_page(60 * 1)(PostListApiView.as_view()), name="list"),  # basit önbellek kullanımı.
    path("detail/<slug>", PostDetailAPIView.as_view(), name="detail"),
    path("update/<slug>", PostUpdateAPIView.as_view(), name="delete"),
    path("create/", PostCreateAPIView.as_view(), name="create"),
]
