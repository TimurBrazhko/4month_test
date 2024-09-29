from django.urls import path
from task.views import task_list_view, task_detail_view, task_create_view

urlpatterns = [
    path('tasks/', task_list_view, name='task_list'),
    path('tasks/<int:task_id>/', task_detail_view, name='task_detail'),
    path('tasks/create/', task_create_view, name='task_create'),
]
