from rest_framework import serializers
from post.api.views import Post

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(        # url oluşturduk - detail url'ine yönlendirdik.
        view_name='post:detail',  # namespace:name
        lookup_field='slug'
    )
    username = serializers.SerializerMethodField(method_name='username_new')      # postun bir usename field'i yok. post objesinin userının usernami var.
    class Meta:
        model = Post
        fields=[
            'username',
            'title',
            'content',
            'image',
            'url',
            'created',
            'modified_by'
        ]
    def username_new(self,obj):        # obj = serilazer edilen obje
        return str(obj.user.username)

class PostUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields=[
            'title',
            'content',
            'image',
        ]

    #def validate_title(self, value):  # bir değer için işlem yapar.
    #    if value == 'gul':
   # #        raise serializers.ValidationError('bu değer olmaz !')
    #    return value

    #def validate(self, attrs):   # bütün değerler için işlem yapar.
    #    if attrs['title'] == 'gul':
   #         raise serializers.ValidationError('olmaz !')
   #     return attrs
#
