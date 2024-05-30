from django.db import models

# Create your models here.


class Teacher(models.Model):
    teacherId = models.IntegerField(primary_key=True, auto_created=True)
    teacherName = models.CharField(max_length=100)
    teacherEmail = models.CharField(max_length=100)
    teacherPhone = models.CharField(max_length=12)
    password = models.CharField(max_length=100)


class User(models.Model):
    userId = models.IntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    teacherId = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)


class Admin(models.Model):
    adminId = models.IntegerField(primary_key=True, auto_created=True)
    adminName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Question(models.Model):
    class Choices(models.TextChoices):
        CHOICE_A = 'A'
        CHOICE_B = 'B'
        CHOICE_C = 'C'
        CHOICE_D = 'D'

    questionId = models.IntegerField(primary_key=True, auto_created=True)
    question = models.CharField(max_length=100)
    choice_a = models.CharField(max_length=100)
    choice_b = models.CharField(max_length=100)
    choice_c = models.CharField(max_length=100)
    choice_d = models.CharField(max_length=100)
    answer = models.CharField(max_length=100, choices=Choices.choices)
