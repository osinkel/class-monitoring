from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from timetable.forms import AddSubjectNameForm, UpdateSubjectNameForm
from timetable.logic import get_subjects_name_of_user, get_groups_user_faculty, get_teachers_user_university, \
    get_students_user_group, get_timetables_user_group, get_all_dates_of_week, \
    get_name_of_days, get_all_subjects_of_user_teacher, get_subject_of_user, get_subjects_by_timetable, \
    get_all_subjects_name, get_attendance_user_group
from timetable.models import Timetable, Profile, Group, SubjectName

MAX_CLASSES_IN_DAY = 5


def index(request):
    return render(request, 'timetable/index.html')


class TeacherListView(LoginRequiredMixin, generic.ListView):
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teacher_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_teachers_user_university(self.request.user)


class TeacherDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'teachers/teacher_detail.html'
    login_url = '/accounts/login/'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_subjects'] = get_all_subjects_of_user_teacher(self.request.user, context['object'])
        return context


class GroupListView(LoginRequiredMixin, generic.ListView):
    template_name = 'groups/group_list.html'
    context_object_name = 'group_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_groups_user_faculty(self.request.user)


class GroupDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'groups/group_detail.html'
    login_url = '/accounts/login/'
    model = Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = get_students_user_group(self.request.user)
        return context


class SubjectNameListView(LoginRequiredMixin, generic.ListView):
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subject_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return get_all_subjects_name()
        return get_subjects_name_of_user(self.request.user)


class SubjectNameDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'subjects/subject_detail.html'
    login_url = '/accounts/login/'
    model = SubjectName

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = get_subject_of_user(self.request.user, context['object'])
        return context


class SubjectNameCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'subjects/subject_create_form.html'
    model = SubjectName
    form_class = AddSubjectNameForm
    success_url = '/timetable/subjects'


class SubjectNameDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'subjects/subject_confirm_delete.html'
    model = SubjectName
    success_url = '/timetable/subjects'


class SubjectNameUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'subjects/subject_update_form.html'
    model = SubjectName
    form_class = UpdateSubjectNameForm
    success_url = '/timetable/subjects'


class TimetableListView(LoginRequiredMixin, generic.ListView):
    template_name = 'timetable/index.html'
    context_object_name = 'timetable_list'
    login_url = '/accounts/login/'
    permission_required = 'timetable.view_timetable'

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return []
        return get_timetables_user_group(self.request.user)[::-1]


class TimetableDetailView(LoginRequiredMixin, generic.DetailView):
    model = Timetable
    template_name = 'timetable/timetable_detail.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.handle_no_permission()
        context = super().get_context_data(**kwargs)
        context['timetable_list'] = get_timetables_user_group(self.request.user)[::-1]
        context['students'] = get_students_user_group(self.request.user)
        context['days'] = get_all_dates_of_week(context['object'])
        context['days_name'] = get_name_of_days(context['object'])
        context['subjects'] = get_subjects_by_timetable(context['object'], MAX_CLASSES_IN_DAY)
        context['attendance'] = get_attendance_user_group(context['students'],
                                                          context['subjects'],
                                                          max_classes_in_day=MAX_CLASSES_IN_DAY)
        context['max_classes_in_day'] = MAX_CLASSES_IN_DAY
        return context
