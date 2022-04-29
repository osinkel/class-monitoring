import datetime

from django.contrib.auth.models import User

from timetable.models import Profile, SubjectName, AllowedRoles, Timetable, Subject, Group


def get_profile(user: User) -> Profile:
    return Profile.objects.filter(user=user)[:1].get()


def get_subjects_name_of_user(user: User) -> set:
    current_profile = get_profile(user)
    all_user_subject = Subject.objects.filter(group=current_profile.group)
    return {subject.name for subject in all_user_subject}


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
    subjects = Subject.objects.filter(timetable=timetable)[:max_classes_in_day]
    prepared_subjects_for_timetable = []

    for date in get_all_dates_of_week(timetable):
        prepared_subjects_for_timetable.append(fill_day_by_subjects(date, subjects, max_classes_in_day))
    return prepared_subjects_for_timetable


def fill_day_by_subjects(date: str, subjects: list[Subject], max_classes_in_day: int) -> list:
    subjects_of_one_day = []
    for subject in subjects:
        if subject.date.strftime('%d.%m.%Y') == date:
            subjects_of_one_day.append(subject)

    number_of_missing_subjects = max_classes_in_day - len(subjects_of_one_day)

    subjects_of_one_day = subjects_of_one_day[:] + ([None] * number_of_missing_subjects)[:]
    return subjects_of_one_day


def get_attendance_user_group(students: list[Profile], subjects_of_week: list[Subject | None], max_classes_in_day: int = 5) -> list:
    attendance_list = []
    for student in students:
        attendance_one_student = [f"{student.user.last_name} {student.user.first_name}"]
        for subjects_of_day in subjects_of_week:
            if len(attendance_one_student) == (max_classes_in_day * len(subjects_of_week))+1:
                break
            attendance_one_student = attendance_one_student + get_student_attendance_of_one_day(student, subjects_of_day)
        attendance_list.append(attendance_one_student)
    return attendance_list


def get_student_attendance_of_one_day(student: Profile, subjects: list[Subject | None]) -> list:
    attendance_one_student_day = []
    for subject in subjects:
        if isinstance(subject, Subject):
            absence = subject.absences.filter(student=student)
            if absence:
                if absence[0].is_good_cause:
                    attendance_one_student_day.append("н'")
                else:
                    attendance_one_student_day.append("н")
            else:
                attendance_one_student_day.append(' ')
        else:
            attendance_one_student_day.append(' ')

    return attendance_one_student_day


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
