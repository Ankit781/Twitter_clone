from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class tweet(models.Model):
    user = models.ForeignKey(
        User, related_name="tweets",
        on_delete= models.DO_NOTHING
    )
    body = models.CharField(max_length= 200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="tweets_like", blank = True)
    
    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return (
            f'{self.user}'
            f'{self.created_at: %Y-%m-%d %H:%M}'  
            f'{self.body}...'  
                   
        )
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False,blank = True)
    date_modified = models.DateTimeField(User, auto_now= True)
    profile_img = models.ImageField(null = True, blank = True, upload_to= "static/img/") 
    def __str__(self):
        return self.user.username
    
    
# Create user when new user signs up
@receiver(post_save,sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
            user_profile = Profile(user = instance)
            user_profile.save()
            user_profile.follows.set([instance.profile.id])
            user_profile.save()
# post_save.connect(create_profile, sender=User)

    
    