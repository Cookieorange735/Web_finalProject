from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    last_updated = models.DateTimeField(default=timezone.now)  # <-- 新增欄位

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
    
    def update_status(self):
        now = timezone.now()
        elapsed = (now - self.last_updated).total_seconds() / 60  # 分鐘
        if elapsed >= 1:
            decay = int(elapsed)
            self.hunger = max(0, self.hunger - decay)
            self.happiness = max(0, self.happiness - decay)
            self.cleanliness = max(0, self.cleanliness - decay)
            self.last_updated = now
            self.save()
