
from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views
from myapp import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('django.contrib.auth.urls')),
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("", emp_home),
    path("home/",emp_home),
    path("add-emp/",add_emp),
    path("delete-emp/<int:emp_id>",delete_emp),
    path("update-emp/<int:emp_id>",update_emp),
    path("do-update-emp/<int:emp_id>",do_update_emp),
    path("emp_profile/<int:emp_id>", emp_profile),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/add/', add_task, name='add_task'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/mark/', mark_attendance, name='mark_attendance'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
    path('tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task')'''

