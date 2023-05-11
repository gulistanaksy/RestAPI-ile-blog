from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from post.models import Post


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies')    # bir yorum başka bir yorum altında olabilir.
    created = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.post.title+ " "+ self.user.username

    def save(self, *args, **kwargs):      # sadece ilk oluşturulduğunda created ı düzenler - modifield sürekli düzenlenir
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Comment,self).save(*args,**kwargs)

    def children(self):   # kendi altındaki yorumları bulmak için.
        return Comment.objects.filter(parent=self)
    @property
    def any_children(self):
        return Comment.objects.filter(parent=self).exists()      # hiç çocuğu ver mı?