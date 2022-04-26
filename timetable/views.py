from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from timetable.logic import get_subjects_name_of_user, get_groups_user_faculty, get_teachers_user_university, \
    get_students_user_group, get_timetables_user_group, get_subjects_user_group_by_date, \
    get_attendance_user_group_by_date, get_all_dates_of_week, get_name_of_days

MAX_CLASSES_IN_DAY = 5

def index(request):
    return render(request, 'timetable/index.html')


class TeacherListView(LoginRequiredMixin, generic.ListView):
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teacher_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_teachers_user_university(self.request.user)


class GroupListView(LoginRequiredMixin, generic.ListView):
    template_name = 'groups/group_list.html'
    context_object_name = 'group_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_groups_user_faculty(self.request.user)


class SubjectListView(LoginRequiredMixin, generic.ListView):
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subject_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_subjects_name_of_user(self.request.user)


class TimetableListView(LoginRequiredMixin, generic.ListView):
    template_name = 'timetable/index.html'
    context_object_name = 'timetable_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_timetables_user_group(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = get_students_user_group(self.request.user)
        last_week = context['timetable_list'][0]
        context['days'] = get_all_dates_of_week(last_week)
        context['days_name'] = get_name_of_days(last_week)
        context['subjects'] = get_subjects_user_group_by_date(self.request.user, last_week, max_classes_in_day=MAX_CLASSES_IN_DAY)
        context['attendance'] = get_attendance_user_group_by_date(context['students'], context['subjects'], max_classes_in_day=MAX_CLASSES_IN_DAY)
        context['max_classes_in_day'] = MAX_CLASSES_IN_DAY
        print(context['attendance'])
        return context
