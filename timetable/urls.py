from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # path('', views.index, name='index'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('subjects/', views.SubjectListView.as_view(), name='subjects'),
    path('', views.TimetableListView.as_view(), name='timetable')
]