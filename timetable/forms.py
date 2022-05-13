import datetime

from django import forms
from django.core.exceptions import ValidationError
from timetable.models import Subject, Profile, AllowedRoles, Timetable


class AddSubjectForm(forms.ModelForm):
    group = forms.IntegerField(widget=forms.HiddenInput())

    teacher = forms.ModelChoiceField(queryset=Profile.objects.filter(role=AllowedRoles.LECTURER))

    timetable = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Subject
        fields = ('name', 'type', 'time', 'date')

        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.date.today() - datetime.timedelta(days=(7*4) + datetime.date.today().weekday()),
                'max': datetime.date.today()
            })
        }
