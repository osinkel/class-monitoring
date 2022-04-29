from django.db import models
from django.contrib.auth.models import User


class AllowedRoles(models.TextChoices):
    """All possible roles in system.
    STUDENT is ordinary student of some university. View only his classes.
    PRESIDENT is the head of the student group. His task is to mark the presence of students.
    LECUTRER is teacher. He can view the students' presence on his classes.
    OTHER - people, who do not belong to any of the previous groups, for example,
    dean, deputy dean or head teacher etc."""

    STUDENT = 'student'
    PRESIDENT = 'president'
    LECTURER = 'lecturer'
    OTHER = 'other'


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=AllowedRoles.choices, max_length=20)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__last_name']

    def __str__(self):
        return str(self.user)


class Timetable(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField('дата')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.group)+', '+str(self.date)


class Lecturer(models.Model):
    first_name = models.CharField('имя', max_length=50)
    last_name = models.CharField('фамилия', max_length=50)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.last_name


class SubjectName(models.Model):
    name = models.CharField('название', max_length=255)
    short_name = models.CharField('сокращенное название', max_length=50)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

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
        return str(self.time)


class StudentAttendance(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_good_cause = models.BooleanField('уважительная причина', default=False)
    cause = models.CharField('причина', max_length=255, default='прогул')

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return str(self.student)+', '+str(self.cause)


class Subject(models.Model):
    name = models.ForeignKey(SubjectName, on_delete=models.CASCADE)
    type = models.ForeignKey(SubjectType, on_delete=models.CASCADE)
    time = models.ForeignKey(SubjectTime, on_delete=models.CASCADE)
    absences = models.ManyToManyField(StudentAttendance)
    date = models.DateField('дата')
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', 'time']

    def __str__(self):
        return f"{str(self.name)}, {self.time}, {str(self.date)}"
