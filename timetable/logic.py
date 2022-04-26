import datetime

from django.contrib.auth.models import User
from django.db.models import DateField

from timetable.models import Profile, SubjectName, AllowedRoles, Timetable, Subject, StudentAttendance


def get_subjects_name_of_user(user) -> list:
    current_profile = Profile.objects.filter(user=user)[:1].get()
    subjects_name_all = SubjectName.objects.all()
    subjects_name_user_group = []
    for subject in subjects_name_all:
        if current_profile.group in subject.groups.all():
            subjects_name_user_group.append(subject)
    return subjects_name_user_group


def get_teachers_user_university(user) -> list:
    current_profile = Profile.objects.filter(user=user)[:1].get()
    return Profile.objects.filter(role=AllowedRoles.LECTURER, university=current_profile.university)


def get_groups_user_faculty(user) -> list:
    current_profile = Profile.objects.filter(user=user)[:1].get()
    return current_profile.faculty.groups.all()


def get_students_user_group(user) -> list:
    current_profile = Profile.objects.filter(user=user)[:1].get()
    return Profile.objects.filter(
        university=current_profile.university,
        faculty=current_profile.faculty,
        group=current_profile.group
    )


def get_timetables_user_group(user) -> list:
    current_profile = Profile.objects.filter(user=user)[:1].get()
    return Timetable.objects.filter(group=current_profile.group)


def get_subjects_user_group(user) -> list:
    current_profile = Profile.objects.filter(user=user)[:1].get()
    return Subject.objects.filter(group=current_profile.group)


def get_subjects_user_group_by_date(user: User, timetable: Timetable, max_classes_in_day: int = 5):
    current_profile = Profile.objects.filter(user=user)[:1].get()
    to_date = timetable.date + datetime.timedelta(days=6)
    subjects = Subject.objects.filter(group=current_profile.group, date__gte=timetable.date,
                           date__lte=to_date)
    if len(subjects)>max_classes_in_day:
        return subjects[:5]
    return subjects


def get_attendance_user_group_by_date(students: list[Profile], subjects: list[Subject], max_classes_in_day: int = 5) -> list:
    attendance_list = []
    for student in students:
        attendance_one_student = [f"{student.user.last_name} {student.user.first_name}"]
        for subject in subjects:
            if len(attendance_one_student) == max_classes_in_day+1:
                break

            absence = subject.absences.filter(student=student)
            if absence:
                if absence[0].is_good_cause:
                    attendance_one_student.append("н'")
                else:
                    attendance_one_student.append("н")
            else:
                attendance_one_student.append(' ')
        attendance_list.append(attendance_one_student)
    return attendance_list


def get_all_dates_of_week(week: Timetable) -> list:
    result = []
    for x in range(6):
        result.append((week.date + datetime.timedelta(days=x)).strftime('%d.%m.%Y'))
    return result


def get_name_of_days(week: Timetable) -> list:
    days_translates = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье',
    }
    result = []
    for x in range(6):
        result.append(days_translates[(week.date + datetime.timedelta(days=x)).strftime("%A")])
    return result
