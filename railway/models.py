from django.db import models


class BotAdmin(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    telegram_id = models.CharField(max_length=255, unique=True)
    tg_username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.username} (ID: {self.telegram_id})"