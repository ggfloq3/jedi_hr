from django.db import models

# Create your models here.
from django.urls import reverse


class Planet(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Jedi(models.Model):
    name = models.CharField(max_length=32)
    planet = models.ForeignKey(Planet)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jedi_detail', args=[self.id])


class Candidate(models.Model):
    name = models.CharField(max_length=32)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(unique=True)
    planet = models.ForeignKey(Planet)
    jedi_master = models.ForeignKey(Jedi, null=True, blank=True)

    def get_quiz(self):
        # получаем нужный тест для кандидата
        return Quiz.objects.first()

    def __str__(self):
        return self.name


class Quiz(models.Model):
    code = models.PositiveSmallIntegerField()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    text = models.CharField(max_length=128)
    right_answer = models.BooleanField(verbose_name='Отметьте если правильный ответ - "Да"')


class CandidateAnswer(models.Model):
    candidate = models.ForeignKey(Candidate)
    question = models.ForeignKey(Question)
    answer = models.BooleanField()

    @property
    def is_right(self):
        return self.answer == self.question.right_answer

    def __str__(self):
        return '{} - {}'.format(self.candidate.name, self.question.text)
