from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('teachers/<int:pk>', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('groups/<int:pk>', views.GroupDetailView.as_view(), name='group_detail'),
    path('subjects/', views.SubjectNameListView.as_view(), name='subjects'),
    path('subjects/<int:pk>', views.SubjectNameDetailView.as_view(), name='subject_detail'),
    path('<int:pk>', views.TimetableDetailView.as_view(), name='timetable_detail'),
    path('<int:timetable_id>/create_subject', views.timetable_create_subject, name='timetable_subject_create'),
    path('create', views.create_timetable, name='timetable_create'),
    path('', views.TimetableListView.as_view(), name='timetable')
]