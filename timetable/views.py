import datetime
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from timetable.forms import AddSubjectForm, UpdateSubjectForm
from timetable.logic import get_subjects_name_of_user, get_groups_user_faculty, get_teachers_user_university, \
    get_students_user_group, get_timetables_user_group, get_all_dates_of_week, get_name_of_days, \
    get_all_subjects_of_user_teacher, get_subject_of_user, get_subjects_by_timetable, get_attendance_user_group, \
    create_timetable_for_group, get_timetable_by_id, \
    create_subject_for_timetable, do_subject_create_form
from timetable.models import Timetable, Profile, Group, SubjectName, Subject

MAX_CLASSES_IN_DAY = 5


def index(request):
    return render(request, 'timetable/index.html')


class TeacherListView(LoginRequiredMixin, generic.ListView):
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teacher_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_teachers_user_university(self.request.user)

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return redirect('/admin/')
        return super(TeacherListView, self).get(*args, **kwargs)


class TeacherDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'teachers/teacher_detail.html'
    login_url = '/accounts/login/'
    model = Profile

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context['teacher_subjects'] = get_all_subjects_of_user_teacher(self.request.user, context['object'])
        return context


class GroupListView(LoginRequiredMixin, generic.ListView):
    template_name = 'groups/group_list.html'
    context_object_name = 'group_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_groups_user_faculty(self.request.user)

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return redirect('/admin/')
        return super(GroupListView, self).get(*args, **kwargs)


class GroupDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'groups/group_detail.html'
    login_url = '/accounts/login/'
    model = Group

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context['students'] = get_students_user_group(self.request.user)
        return context


class SubjectNameListView(LoginRequiredMixin, generic.ListView):
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subject_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return get_subjects_name_of_user(self.request.user)

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return redirect('/admin/')
        return super(SubjectNameListView, self).get(*args, **kwargs)


class SubjectNameDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'subjects/subject_detail.html'
    login_url = '/accounts/login/'
    model = SubjectName

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context['subjects'] = get_subject_of_user(self.request.user, context['object'])
        return context


class TimetableListView(LoginRequiredMixin, generic.ListView):
    template_name = 'timetable/index.html'
    context_object_name = 'timetable_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return []
        return get_timetables_user_group(self.request.user)[::-1]

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return redirect('/admin/')
        return super(TimetableListView, self).get(*args, **kwargs)


class TimetableDetailView(LoginRequiredMixin, generic.DetailView):
    model = Timetable
    template_name = 'timetable/timetable_detail.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context = context_for_timetable_detail_view(self.request.user, context['object'], context=context)
        return context


def context_for_timetable_detail_view(user: User, timetable: Timetable, context: dict = None):
    if context is None:
        context = dict()
        context['object'] = timetable
    context['timetable_list'] = get_timetables_user_group(user)[::-1]
    context['students'] = get_students_user_group(user)
    context['days'] = get_all_dates_of_week(context['object'])
    context['days_name'] = get_name_of_days(context['object'])
    context['subjects'] = get_subjects_by_timetable(context['object'], MAX_CLASSES_IN_DAY)
    context['attendance'] = get_attendance_user_group(context['students'],
                                                      context['subjects'],
                                                      max_classes_in_day=MAX_CLASSES_IN_DAY)
    context['max_classes_in_day'] = MAX_CLASSES_IN_DAY
    context['subject_create_form'] = do_subject_create_form(user, context['object'].id)
    return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def create_timetable(request):
    if is_ajax(request):
        if request.method == 'POST':
            json_data = json.loads(request.body.decode("utf-8"))
            try:
                timetable_id = int(json_data['id'])
            except KeyError as exc:
                return JsonResponse({'status': 'failed', 'error': exc})
            day = get_timetable_by_id(timetable_id).date + datetime.timedelta(days=7)
            try:
                new_timetable = create_timetable_for_group(request.user, day)
            except:
                return JsonResponse({'status': 'error'})
            return JsonResponse({'status': 'success', 'id': new_timetable.id, 'date': new_timetable.date})


def timetable_get_subject(request):
    if is_ajax(request):
        if request.method == 'GET':
            try:
                subject = Subject.objects.get(pk=request.GET.get('id', 0))
            except:
                return JsonResponse({'status': 'error'})
            return JsonResponse({
                'status': 'success',
                'name': subject.name.name,
                'short_name': subject.name.short_name,
                'type': subject.type.name,
                'date': subject.date,
                'time': subject.time.time,
            })


def timetable_delete_subject(request):
    if is_ajax(request):
        if request.method == 'GET':
            try:
                subject = Subject.objects.get(pk=request.GET.get('id', 0))
                subject.delete()
            except ObjectDoesNotExist as exc:
                return JsonResponse({'status': 'error', 'msg': str(exc)})
            return JsonResponse({
                'status': 'success',
            })


def timetable_create_subject(request, timetable_id):
    if request.method == 'POST':

        form = AddSubjectForm(request.POST)
        if form.is_valid():
            try:
                create_subject_for_timetable(form.cleaned_data)
            except ValueError as exc:
                print(exc)

    return HttpResponseRedirect(reverse('timetable:timetable_detail', args=(timetable_id,)))


class SubjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'subjects/subject_update_form.html'
    model = Subject
    form_class = UpdateSubjectForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(SubjectUpdateView, self).get_form_kwargs()
        redirect = self.request.GET.get('next')
        if redirect:
            if 'initial' in kwargs.keys():
                kwargs['initial'].update({'next': redirect})
            else:
                kwargs['initial'] = {'next': redirect}
        return kwargs

    def form_invalid(self, form):
        return super(SubjectUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        print(form.cleaned_data.get('date'), type(form.cleaned_data.get('date')))
        redirect = form.cleaned_data.get('next')
        if redirect:
            self.success_url = redirect
        return super(SubjectUpdateView, self).form_valid(form)
