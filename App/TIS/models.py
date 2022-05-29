from django.db import models


class NumGroup(models.Model):
    num_group = models.CharField(max_length=50, primary_key=True, verbose_name="Номер группы")


class Student(models.Model):
    surname = models.CharField(max_length=50, verbose_name="Фамилия")
    name = models.CharField(max_length=50, verbose_name="Имя")
    patronymic = models.CharField(max_length=50, verbose_name="Отчество")
    login = models.CharField(max_length=50, verbose_name="Логин")
    password = models.CharField(max_length=50, verbose_name="Пароль", )
    num_group = models.ForeignKey(NumGroup, on_delete=models.CASCADE, verbose_name="Номер группы")


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=200)


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    id_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class Question(models.Model):
    question = models.CharField(max_length=200)
    id_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Answer(models.Model):
    answer = models.CharField(max_length=200)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerStudent(models.Model):
    ans_stud = models.CharField(max_length=200)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_student = models.ForeignKey(Student, on_delete=models.CASCADE)


class TheorMat(models.Model):
    id_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    theor_mat = models.CharField(max_length=200)
