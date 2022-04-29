from django import forms

from timetable.models import SubjectName, Group, Profile


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


class AddGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', )

        widgets = {
            'name': forms.TextInput(),
        }


class UpdateGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name',)


class AddTeacherForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('user', 'group', 'university', 'faculty', 'role')

        widgets = {
            'name': forms.TextInput(),
        }


class UpdateTeacherForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('user', 'group', 'university', 'faculty', 'role')
