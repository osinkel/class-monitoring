import datetime

from django import forms
from timetable.models import Subject, Profile, AllowedRoles


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


class UpdateSubjectForm(forms.ModelForm):
    next = forms.CharField(required=False, widget=forms.HiddenInput())
    teacher = forms.ModelChoiceField(queryset=Profile.objects.filter(role=AllowedRoles.LECTURER))

    class Meta:
        model = Subject
        fields = ('name', 'type', 'time', 'date', 'teacher')
