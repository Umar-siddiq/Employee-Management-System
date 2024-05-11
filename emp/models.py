from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Emp(models.Model):
    name=models.CharField(max_length=200)
    emp_id=models.CharField(max_length=200)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=150)
    working=models.BooleanField(default=True)
    department=models.CharField(max_length=200)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)  # Stores photos in MEDIA_ROOT/employee_photos

    def __str__(self):
        return self.name


class Attendance(models.Model):
    employee = models.ForeignKey(Emp, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)  # True for Present, False for Absent

    class Meta:
        unique_together = ('employee', 'date')  # Ensure one entry per employee per day

    def __str__(self):
        return f"{self.employee.name} - {'Present' if self.status else 'Absent'} on {self.date}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ChecklistItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='checklist_items')
    text = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text