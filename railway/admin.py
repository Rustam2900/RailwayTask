from django.contrib import admin
from railway.models import BotAdmin


@admin.register(BotAdmin)
class BotAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'username', 'full_name', 'tg_username')
    search_fields = ('id', 'username', 'tg_username', 'telegram_id')
