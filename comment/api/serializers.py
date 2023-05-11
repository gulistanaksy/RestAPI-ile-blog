from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from comment.models import Comment
from django.contrib.auth.models import User

from post.models import Post


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created']  # created hariç bütün fieldleri kabul et.

    def validate(self, attrs):
        if attrs["parent"]:                                                    # parent seçilmiş mi?
            if attrs["parent"].post != attrs["post"]:                          # parent ile kendi postu aynı mı?
                raise serializers.ValidationError("something went wrong")
        return attrs

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','id','email')      # sadece user id si gözükmesin, burada belirttiğimiz değerler görünsün.

class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','slug','id')

class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserSerializer()
    post = PostCommentSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
        #depth =1   # ForeignKey olarak bağlı olanların bütün bilgilerini getirir.

    def get_replies(self, obj):
        if obj.any_children:             # @property kısmını kullandık.  - hiç çocuğu var mı
            return CommentListSerializer(obj.children(), many=True).data  # çocuğu varsa getir.

class CommentDeleteUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]
