from timetable.models import Profile, SubjectName


def get_subjects_name_of_user(user) -> list:
    current_profile = Profile.objects.filter(user=user)[:1].get()
    subjects_name_all = SubjectName.objects.all()
    subjects_name_user_group = []
    for subject in subjects_name_all:
        if current_profile.group in subject.groups.all():
            subjects_name_user_group.append(subject)
    return subjects_name_user_group
