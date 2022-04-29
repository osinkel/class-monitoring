from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # path('', views.index, name='index'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('teachers/<int:pk>', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('groups/<int:pk>', views.GroupDetailView.as_view(), name='group_detail'),
    path('subjects/', views.SubjectNameListView.as_view(), name='subjects'),
    path('subjects/delete/<int:pk>/', views.SubjectNameDeleteView.as_view(), name='subject_delete'),
    path('subjects/update/<int:pk>/', views.SubjectNameUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>', views.SubjectNameDetailView.as_view(), name='subject_detail'),
    path('subjects/create', views.SubjectNameCreateView.as_view(), name='subject_create'),
    path('<int:pk>', views.TimetableDetailView.as_view(), name='timetable_detail'),
    path('', views.TimetableListView.as_view(), name='timetable')
]