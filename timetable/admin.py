from django.contrib import admin
from .models import Profile, Group, Faculty, University, Subject, SubjectName, SubjectTime, SubjectType, StudentAttendance, Timetable, Lecturer

admin.site.register(Profile)
admin.site.register(Faculty)
admin.site.register(University)
admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(SubjectName)
admin.site.register(SubjectType)
admin.site.register(SubjectTime)
admin.site.register(StudentAttendance)
admin.site.register(Timetable)
admin.site.register(Lecturer)

