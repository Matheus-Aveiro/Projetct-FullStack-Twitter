from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class tweet(models.Model):
    user = models.ForeignKey(
        User, related_name="tweets",
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at: %Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', 
                                    related_name='followed_by',
                                    symmetrical=False,
                                    blank=True)
    datee_modified = models.DateTimeField(User, auto_now=True)
    
    def __str__(self):
        return self.user.username
    
# @receiver(post_save, sender=User)    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)