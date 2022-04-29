from django import forms

from timetable.models import SubjectName, Faculty


class AddSubjectNameForm(forms.ModelForm):

    class Meta:
        model = SubjectName
        fields = ('name', 'short_name', 'faculty')

        widgets = {
            'name': forms.TextInput(),
            'short_name': forms.TextInput(),
        }


class UpdateSubjectNameForm(forms.ModelForm):

    class Meta:
        model = SubjectName
        fields = ('name', 'short_name', 'faculty')
