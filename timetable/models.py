from django.db import models
from django.contrib.auth.models import User


class AllowedRoles(models.TextChoices):
    STUDENT = 'student'
    LECTURER = 'lecturer'
    OTHER = 'other'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=AllowedRoles.choices, max_length=20)

    def __str__(self):
        return self.user.name


class Group(models.Model):
    name = models.CharField('название', max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Faculty(models.Model):
    groups = models.ManyToManyField(Group)
    name = models.CharField('название', max_length=255)

    def __str__(self):
        return self.name


class University(models.Model):
    faculties = models.ManyToManyField(Faculty)
    name = models.CharField('название', max_length=255)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateTimeField('дата')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.group


class Lecturer(models.Model):
    first_name = models.CharField('имя', max_length=50)
    last_name = models.CharField('фамилия', max_length=50)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.last_name


class SubjectName(models.Model):
    name = models.CharField('предмет', max_length=255)
    duration = models.SmallIntegerField('количество часов')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SubjectType(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField('название', max_length=20)

    def __str__(self):
        return self.name


class SubjectTime(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    time = models.TimeField('время начала')

    class Meta:
        ordering = ['university', 'time']

    def __str__(self):
        return self.time


class Subject(models.Model):
    name = models.ForeignKey(SubjectName, on_delete=models.CASCADE)
    type = models.ForeignKey(SubjectType, on_delete=models.CASCADE)
    time = models.ForeignKey(SubjectTime, on_delete=models.CASCADE)
    date = models.DateField('дата')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', 'time']

    def __str__(self):
        return self.date


class StudentAttendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    presence = models.BooleanField('присутствие')

    class Meta:
        ordering = ['student', 'subject']

    def __str__(self):
        return self.presence
