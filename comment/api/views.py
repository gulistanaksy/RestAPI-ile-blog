from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import DestroyModelMixin

from comment.api.paginations import CommentPagination
from comment.api.permissions import IsOwner
from comment.api.serializers import CommentCreateSerializer, CommentListSerializer, CommentDeleteUpdateSerializer
from comment.models import Comment


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination
    def get_queryset(self):
        queryset = Comment.objects.filter(parent= None)                    # ilk(parent) yorumlar gelicek.
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(post=query)
        return queryset


class CommentUpdateAPIView(DestroyModelMixin, RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)    # delete butonuna basıldığında destroy u çalıştırıyoruz.


#class CommentDeleteAPIView(DestroyAPIView):
#    queryset = Comment.objects.all()
#    serializer_class = CommentDeleteUpdateSerializer
#    lookup_field = 'pk'
#    permission_classes = [IsOwner]
#