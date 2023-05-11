from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin

from post.api.paginations import PostPagination
from post.models import Post
from post.api.serializers import PostSerializer, PostUpdateCreateSerializer
from post.api.permissions import IsOwner

class PostListApiView(ListAPIView):        # bütün postları listeleriz.
    serializer_class = PostSerializer
    # arama
    filter_backends = [SearchFilter, OrderingFilter]     # ?ordering=-user dersek user'a göre sıralama yapar.
    search_fields = ['title','content']     # nelerin içinde arama yapsın.
    pagination_class = PostPagination
    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset


class PostDetailAPIView(RetrieveAPIView):  # slug'a göre detay getirir.
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):  # PostUpdateAPIView yerine, RetrieveUpdateAPIView kullanırsak form dolu gelir.
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]
    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer

    def perform_create(self, serializer):        # oluşturulurken bunları yap.
        serializer.save(user=self.request.user)  # save etmeyi unutma