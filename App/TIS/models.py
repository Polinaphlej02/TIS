from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class NumGroup(models.Model):
    num_group = models.CharField(max_length=50, primary_key=True, verbose_name="Номер группы")


class Student(AbstractUser):
    username = models.CharField(max_length=150, verbose_name="Логин", unique=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    patronymic = models.CharField(max_length=50, verbose_name="Отчество")
    num_group = models.ForeignKey(NumGroup, on_delete=models.CASCADE, verbose_name="Номер группы")

    REQUIRED_FIELDS = ["num_group_id"]


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=200)


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    id_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class Question(models.Model):
    question = models.CharField(max_length=200)
    id_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class QuestionMini(models.Model):
    question = models.CharField(max_length=200)


class Answer(models.Model):
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    id_question = models.ForeignKey(QuestionMini, on_delete=models.CASCADE)


class AnswerStudent(models.Model):
    ans_stud = models.CharField(max_length=200)
    id_question = models.ForeignKey(QuestionMini, on_delete=models.CASCADE)
    id_student = models.ForeignKey(Student, on_delete=models.CASCADE)


class TheorMat(models.Model):
    id_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    theor_mat = models.CharField(max_length=60000)
