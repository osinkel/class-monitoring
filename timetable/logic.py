import datetime

from django.contrib.auth.models import User

from timetable.models import Profile, SubjectName, AllowedRoles, Timetable, Subject, Group


def get_profile(user: User) -> Profile:
    return Profile.objects.filter(user=user)[:1].get()


def get_subjects_name_of_user(user: User) -> list:
    subjects_name_all = SubjectName.objects.all()
    subjects_name_user_group = []
    current_profile = get_profile(user)
    for subject in subjects_name_all:
        if current_profile.group in subject.groups.all():
            subjects_name_user_group.append(subject)
    return subjects_name_user_group


def get_subject_of_user(user: User, subject_name: SubjectName) -> list:
    current_profile = get_profile(user)
    return Subject.objects.filter(group=current_profile.group, name=subject_name)


def get_teachers_user_university(user: User) -> list:
    current_profile = get_profile(user)
    return Profile.objects.filter(role=AllowedRoles.LECTURER, university=current_profile.university)


def get_groups_user_faculty(user: User) -> list:
    current_profile = get_profile(user)
    return current_profile.faculty.groups.all()


def get_students_user_group(user) -> list:
    current_profile = get_profile(user)
    return Profile.objects.filter(
        university=current_profile.university,
        faculty=current_profile.faculty,
        group=current_profile.group
    )


def get_timetables_user_group(user: User) -> list:
    current_profile = get_profile(user)
    return Timetable.objects.filter(group=current_profile.group)


def get_subjects_user_group(user: User) -> list:
    current_profile = get_profile(user)
    return Subject.objects.filter(group=current_profile.group)


def get_subjects_by_timetable(timetable: Timetable, max_classes_in_day: int) -> list:
    return Subject.objects.filter(timetable=timetable)[:max_classes_in_day]


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


def get_all_subjects_of_user_teacher(current_user: User, teacher_profile: Profile) -> list:
    current_profile = get_profile(current_user)
    return Subject.objects.filter(teacher=teacher_profile, group=current_profile.group)
