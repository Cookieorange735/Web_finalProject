from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    hunger = models.IntegerField(default=50)       # 0 = 飽, 100 = 餓
    happiness = models.IntegerField(default=50)    # 0 = 難過, 100 = 快樂
    cleanliness = models.IntegerField(default=50)  # 0 = 髒, 100 = 乾淨
    created_at = models.DateTimeField(auto_now_add=True)
    last_interaction = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

