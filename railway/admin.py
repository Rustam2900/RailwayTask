from django.contrib import admin
from .models import User, Test, Question, UserTestResult, UserAnswer


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "full_name", "username", "role", "created_at")
    search_fields = ("telegram_id", "full_name", "username")
    list_filter = ("role", "created_at")
    ordering = ("-created_at",)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "admin", "created_at")
    search_fields = ("title", "admin__full_name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "test", "correct_answer")
    search_fields = ("text", "test__title")
    list_filter = ("test",)
    ordering = ("test",)


@admin.register(UserTestResult)
class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "correct_answers", "total_questions", "score_percentage", "completed", "completed_at")
    search_fields = ("user__full_name", "test__title")
    list_filter = ("completed", "completed_at")
    ordering = ("-completed_at",)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "selected_option", "is_correct")
    search_fields = ("user__full_name", "question__text")
    list_filter = ("is_correct",)
    ordering = ("user",)


# Agar kodni ishlayotgan loyihaga qo'shmoqchi bo'lsangiz, ushbu faylni `admin.py` sifatida saqlang.
