from django import forms
from .models import Task, ChecklistItem, Attendance

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['text']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'status', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
