from django.db import models
from autoslug import AutoSlugField

from django.db.models.aggregates import Count
from random import randint

from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class SingleChoiceQuestion(models.Model):
    author = models.ForeignKey(User)
    question = models.CharField(max_length=255)
    q_slug = AutoSlugField(populate_from='question', unique=True)

    objects = QuestionManager()

    class Meta:
        verbose_name = "SingleChoiceQuestion"

    def __str__(self):
        return self.question


class SingleChoiceOptions(models.Model):
    question = models.ForeignKey('SingleChoiceQuestion', on_delete=models.CASCADE)
    option = models.CharField(max_length=50)

    class Meta:
        verbose_name = "SingleChoiceOptions"

    def __str__(self):
        return self.option


class SingleChoiceAnswer(models.Model):
    question = models.OneToOneField('SingleChoiceQuestion', on_delete=models.CASCADE)
    answer = models.ForeignKey('SingleChoiceOptions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "SingleChoiceAnswer"

    def __str__(self):
        return self.question.question + self.answer.option


class MultiChoiceQuestion(models.Model):
    author = models.ForeignKey(User)
    question = models.CharField(max_length=255)
    q_slug = AutoSlugField(populate_from='question')

    objects = QuestionManager()

    class Meta:
        verbose_name = "MultiChoiceQuestion"

    def __str__(self):
        return self.question


class MultiChoiceOptions(models.Model):
    question = models.ForeignKey('MultiChoiceQuestion', on_delete=models.CASCADE)
    option = models.CharField(max_length=50)

    class Meta:
        verbose_name = "MultiChoiceOptions"

    def __str__(self):
        return self.question.question + self.option


class MultiChoiceAnswers(models.Model):
    question = models.ForeignKey('MultiChoiceQuestion', on_delete=models.CASCADE)
    answers = models.ForeignKey('MultiChoiceOptions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "MultiChoiceAnswers"

    def __str__(self):
        return self.question.question + self.answers.option


class OneWordAnswerType(models.Model):
    author = models.ForeignKey(User)
    question = models.CharField(max_length=255)
    q_slug = AutoSlugField(populate_from='question', unique=True, name='q_slug')
    hint = models.CharField(max_length=60)

    objects = QuestionManager()

    class Meta:
        verbose_name = "OneWordAnswerType"

    def __str__(self):
        return self.question


class OneWordAnswerAnswer(models.Model):
    question = models.OneToOneField('OneWordAnswerType', on_delete=models.CASCADE, related_name='answer')
    answers = models.CharField(max_length=60)

    class Meta:
        verbose_name = "OneWordAnswer_Answer"

    def __str__(self):
        return self.question.question + self.answers
