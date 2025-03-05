from django.db import models
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone


class User(models.Model):
    ADMIN = "admin"
    USER = "user"
    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (USER, "User"),
    ]

    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    contact = models.CharField(max_length=50)
    user_lang = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()}) - ID: {self.telegram_id}"


class Test(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.ADMIN})
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)  # Video bo‘lmasligi mumkin
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.admin.role != User.ADMIN:
            raise PermissionDenied("Faqat adminlar test yaratishi mumkin!")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    options = models.JSONField()  # {"A": "Variant1", "B": "Variant2", "C": "Variant3", "D": "Variant4"}
    correct_answer = models.CharField(max_length=1)  # Masalan: "C"

    def clean(self):
        if self.correct_answer not in self.options.keys():
            raise ValidationError("To‘g‘ri javob variantlardan biri bo‘lishi kerak!")

    def __str__(self):
        return self.text


class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField()
    score_percentage = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'test'], name='unique_user_test_result')
        ]

    def save(self, *args, **kwargs):
        if self.total_questions > 0:
            self.score_percentage = (self.correct_answers / self.total_questions) * 100
        if self.correct_answers == self.total_questions:
            self.completed = True
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.full_name} - {self.test.title} ({self.correct_answers}/{self.total_questions}) - {self.score_percentage:.2f}%"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    selected_option = models.CharField(max_length=1)  # Masalan: "B"
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_option == self.question.correct_answer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.full_name} - {self.question.text} - Javob: {self.selected_option} ({'✅' if self.is_correct else '❌'})"
