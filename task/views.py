from django.shortcuts import render, redirect
from task.forms import SearchForm, CreateForm
from task.models import Task, Category
from django.db.models import Q


def main_page_view(request):
    return render(request, 'base.html')


def task_list_view(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        tasks = Task.objects.all()
        search = request.GET.get('search')
        category = request.GET.getlist('category')

        if search:
            tasks = tasks.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        if category:
            tasks = tasks.filter(category__id__in=category)

        page = request.GET.get('page', 1)
        page = int(page)
        limit = 3
        total_tasks = tasks.count()
        max_pages = (total_tasks + limit - 1) // limit

        if page < 1:
            page = 1
        elif page > max_pages:
            page = max_pages
        start = (page - 1) * limit
        end = start + limit

        tasks = tasks[start:end]

        context = {
            'tasks': tasks,
            'form': form,
            'max_pages': range(1, max_pages + 1),
        }

        return render(request, 'task/task_list.html', context=context)


def task_detail_view(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'GET':
        return render(
            request,
            'task/task_detail.html',
            context={'task': task}
        )


def task_create_view(request):
    if request.method == 'GET':
        form = CreateForm()
        return render(request, "task/task_create.html", context={'form': form})
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if not form.is_valid():
            return render(request, 'task/task_create.html', context={'form': form})
        form.save()
        return redirect("/api/v1/tasks/tasks/")
