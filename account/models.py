from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save   # sinyaller
from django.dispatch import receiver # tetikleme kısmı

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)       # her kullanıcının bir profili olabilir.
    note = models.CharField(max_length=120)
    twitter = models.CharField(max_length=120)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender = User)   # yeni bir kullanıcı eklendiğinde    --   kendiliğinden tetiklenir.
def create_user_profile(sender, instance, created, **kwargs):       # kullanıcı eklendiğinde profil oluştur.
    if created:
        Profile.objects.create(user=instance)     # oluşturdu.
    instance.profile.save()                       # kaydetti.