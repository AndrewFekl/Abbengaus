from django.db import models
from django.conf import settings

# Create your models here.
class Dictonary(models.Model):
    """Словарь слов пользователей с переводом"""
    original_word = models.CharField(max_length=100)
    translated_word = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='WorkTable')

    def __str__(self):
        return self.original_word

class LearningModel(models.Model):
    training_interval = models.SmallIntegerField(default=1)
    comment = models.CharField(max_length=50)

    def __str__(self):
        return self.comment

class WorkTable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Dictonary, on_delete=models.CASCADE)
    current_step = models.SmallIntegerField(default=1)
    training_date = models.DateTimeField('training date')

    def __str__(self):
        return "Word {} for user {}.".format(self.word, self.user)


