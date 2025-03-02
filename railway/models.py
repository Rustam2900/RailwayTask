from django.db import models


class BotAdmin(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    telegram_id = models.CharField(max_length=255, unique=True)
    tg_username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    contact = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user_lang = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Admin: {self.username} (ID: {self.telegram_id})"


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=50)
    username = models.CharField(max_length=255, null=True, blank=True)
    user_lang = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Test(models.Model):
    admin = models.ForeignKey(BotAdmin, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.test.title} ({self.correct_answers}/{self.total_questions})"
