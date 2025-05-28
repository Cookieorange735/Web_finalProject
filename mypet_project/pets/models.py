from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math

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

    def get_time_passed_minutes(self):
        now = timezone.now()
        delta = now - self.last_interaction
        return int(delta.total_seconds() // 60)

    def update_status(self):
        """根據時間差，更新飢餓、快樂、清潔值"""
        minutes = self.get_time_passed_minutes()
        if minutes <= 0:
            return  # 沒過時間就不更新

        # 每分鐘變動的數值（你可以自訂調整速度）
        hunger_increase = minutes * 1
        happiness_decrease = minutes * 0.5
        cleanliness_decrease = minutes * 0.3

        # 新值的計算
        self.hunger = min(self.hunger + hunger_increase, 100)
        self.happiness = max(self.happiness - math.ceil(happiness_decrease), 0)
        self.cleanliness = max(self.cleanliness - math.ceil(cleanliness_decrease), 0)

        self.last_interaction = timezone.now()
        self.save()