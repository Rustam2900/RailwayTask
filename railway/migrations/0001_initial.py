# Generated by Django 4.2 on 2025-03-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('telegram_id', models.CharField(max_length=255, unique=True)),
                ('tg_username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
