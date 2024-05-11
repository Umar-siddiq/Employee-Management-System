from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Emp, Attendance, Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .forms import TaskForm, ChecklistItemForm, AttendanceForm

def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'emp/attendance.html', {'attendances': attendances})

def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            date = form.cleaned_data['date']
            if not date:  
                messages.error(request, "Date is required.")
                return render(request, '/emp/attendance_marking.html', {'form': form})

            if Attendance.objects.filter(employee=employee, date=date).exists():
                messages.error(request, 'Attendance for this employee on this date has already been marked.')
                return redirect('/emp/attendance/')
            else:
                form.save()
                messages.success(request, 'Attendance marked successfully.')
                return redirect('/emp/attendance/')
    else:
        form = AttendanceForm()
    return render(request, 'emp/attendance_marking.html', {'form': form})


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'emp/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    form = ChecklistItemForm()
    if request.method == 'POST':
        form = ChecklistItemForm(request.POST)
        if form.is_valid():
            checklist_item = form.save(commit=False)
            checklist_item.task = task
            checklist_item.save()
            return redirect('task_detail', pk=task.pk)
    return render(request, 'emp/task_detail.html', {'task': task, 'form': form})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'emp/add_task.html', {'form': form})


@login_required
def attendance(request):
    return render(request, "emp/attendance.html")

@login_required
def emp_home(request):
    emps=Emp.objects.all()
    query =  request.GET.get('q','')

    if query :
        emps = Emp.objects.filter(
            Q(name__icontains=query) |
            Q(emp_id__icontains=query) |
            Q(department__icontains=query)
        )

    else:
        emps = Emp.objects.all()


    return render(request,"emp/home.html",{'emps':emps})

@login_required
def add_emp(request):
    if request.method=="POST":
        emp_name=request.POST.get("emp_name")
        emp_id=request.POST.get("emp_id")
        emp_phone=request.POST.get("emp_phone")
        emp_address=request.POST.get("emp_address")
        emp_working=request.POST.get("emp_working")
        emp_department=request.POST.get("emp_department")
        emp_photo=request.POST.get("emp_photo")

        e=Emp()
        e.name=emp_name
        e.emp_id=emp_id
        e.phone=emp_phone
        e.address=emp_address
        e.department=emp_department
        e.photo=emp_photo

        if emp_working is None:
            e.working=False
        else:
            e.working=True
        e.save()
        return redirect("/emp/home/")
    return render(request,"emp/add_emp.html",{})

@login_required
def delete_emp(request,emp_id):
    emp=Emp.objects.get(pk=emp_id)
    emp.delete()
    return redirect("/emp/home/")

@login_required
def update_emp(request,emp_id):
    emp=Emp.objects.get(pk=emp_id)
    print("Yes Bhai")
    return render(request,"emp/update_emp.html",{
        'emp':emp
    })

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Assuming you have a URL named 'task_list' that lists all tasks
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list') 


@login_required
def emp_profile(request, emp_id):
    employee = get_object_or_404(Emp, pk=emp_id)
    return render(request, "emp/emp_profile.html", {'employee':employee})


@login_required
def do_update_emp(request,emp_id):
    if request.method=="POST":
        emp_name=request.POST.get("emp_name")
        emp_id_temp=request.POST.get("emp_id")
        emp_phone=request.POST.get("emp_phone")
        emp_address=request.POST.get("emp_address")
        emp_working=request.POST.get("emp_working")
        emp_department=request.POST.get("emp_department")
        emp_photo = request.POST.get("emp_photo")

        e=Emp.objects.get(pk=emp_id)

        e.name=emp_name
        e.emp_id=emp_id_temp
        e.phone=emp_phone
        e.address=emp_address
        e.department=emp_department
        e.photo=emp_photo
        
        if emp_working is None:
            e.working=False
        else:
            e.working=True
        e.save()
    return redirect("/emp/home/")
