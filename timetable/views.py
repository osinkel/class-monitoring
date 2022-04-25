from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from timetable.logic import get_subjects_name_of_user
from timetable.models import Profile, AllowedRoles, Group, Subject, SubjectName, Faculty


def index(request):
    return render(request, 'timetable/index.html')


class TeacherListView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teacher_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Profile.objects.filter(role=AllowedRoles.LECTURER)


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'groups/group_list.html'
    context_object_name = 'group_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        current_profile = Profile.objects.filter(user=self.request.user)[:1].get()
        return current_profile.faculty.groups.all()


class SubjectListView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subject_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_subjects_name_of_user(self.request.user)
