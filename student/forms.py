from django import forms
from django.contrib.auth.models import User

from .models import InstructorProfile, StudentProfile, Lesson, Tutorial, Exercise

'''
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']
'''


class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ('title', 'tutorial_type') 
        widgets = {
            'title': forms.TextInput(attrs={'autofocus': 'autofocus', 'placeholder': 'Title for tutorial'}),
            'tutorial_type': forms.HiddenInput(attrs={'id': 'tutorial-type--input'})
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('title', 'order', 'question', 'testcases')
        widgets = {
            'question': forms.Textarea(attrs={'id': 'editor'}),
            'testcases': forms.Textarea(attrs={'id': 'testcases-editor'})
        }
    
    def get_form_type(self):
        return 'ExerciseForm'


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'order', 'markdown', 'exercise_question', 'exercise_ans')
        widgets = {
            'markdown': forms.Textarea(attrs={'id': 'editor'}),
            'exercise_question': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'exercise_ans': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
        }
    
    def get_form_type(self):
        return 'LessonForm'

class LoginForm(forms.Form):
    ROLES = (
        ('S', 'Student'),
        ('I', 'Instructor'),
    )
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLES)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                            widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                            widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']
    

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = ('phone', 'photo')


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('phone', 'photo')