from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import auth, messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.urlresolvers import reverse_lazy
import json
from .forms import ProjectForm, TaskForm, CTaskRegisterForm, CommentForm, RegisterUserForm
from .models import Project, Task, Comment, User, ChildTask
from django.core import serializers


# Checkers
def check_project(user):
    if user.is_active:
        return user.is_project_manager
    else:
        return False


def check_client(user):
    if user.is_active:
        return user.is_client
    else:
        return False


def check_dev(user):
    if user.is_active:
        return user.is_developer
    else:
        return False


# Views
def index(request):
    if request.user.is_authenticated.value:
        return redirect('projectman:dashboard')
    else:
        return render(request, 'projectman/index.html')


def login_user(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect('projectman:dashboard')
    else:
        if request.method == 'POST':

            if request.POST.get('username') is None:
                messages.error(request, "Error en usuario y/o contraseña")
            else:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return redirect('projectman:dashboard')
                else:
                    messages.error(request, "Error en usuario y/o contraseña")
                    return redirect('projectman:login')
        else:
            return render(request, 'projectman/login.html')


class RegisterUser(CreateView):
    model = User
    template_name = 'projectman/registrer_user.html'
    form_class = RegisterUserForm

    def form_valid(self, form):
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usuario = auth.authenticate(username=usuario, password=password)
        auth.login(self.request, usuario)
        return redirect('projectman:login')


@login_required
def dashboard(request):
    return render(request, "projectman/dashboard.html")


def help(request):
    return render(request, 'projectman/help.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('projectman:index')


# Vistas del modelo Project
class ProjectCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_task/project_create.html"

    def test_func(self):
        return check_project(self.request.user)

    success_url = reverse_lazy('projectman:list_project')


class ProjectList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Project
    template_name = 'project_task/project_list.html'

    def test_func(self):
        clie = check_client(self.request.user)
        prod = check_project(self.request.user)
        return prod or clie


class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_task/project_create.html'

    def test_func(self):
        return check_project(self.request.user)

    success_url = reverse_lazy('projectman:list_project')


class ProjectDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'project_task/project_delete.html'

    def test_func(self):
        return check_project(self.request.user)

    success_url = reverse_lazy('projectman:list_project')


class ProjectDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'project_task/project_detail.html'

    def test_func(self):
        return check_project(self.request.user)


# Vistas del modelo Task.
class TaskCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "project_task/task_create.html"
    permission_required = 'projectman.add_task'
    success_url = reverse_lazy('projectman:list_task')

    def form_valid(self, form):
        save = super().form_valid(form)
        task = self.object
        data = form.cleaned_data.get('child_task')
        children =  data.split('\r\n')
        for child in children:
            ChildTask(name=child, task=task).save()
        return save



@login_required
def project_list_filter(request, pk):
    projects = Project.objects.filter(client__user__id=1)
    context = {'projects': projects}
    print (pk)
    return render(request, 'project_task/project_list_filter.html', context)


@login_required
def task_list_filter(request, pk):
    tareas = Task.objects.filter(project=pk)
    context = {'tareas': tareas}
    return render(request, 'project_task/task_list_filter.html', context)


class TaskList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Task
    template_name = 'project_task/task_list.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev

    success_url = reverse_lazy('projectman:list_task')


@login_required
def tasks_json(request):
    datos = [task.json for task in Task.objects.all()]
    return HttpResponse(json.dumps(datos), content_type='application/json')


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project_task/task_create.html'
    success_url = reverse_lazy('projectman:list_task')

    def form_valid(self, form):
        save = super().form_valid(form)
        task = super(TaskUpdate, self).get_object()
        data = form.cleaned_data.get('child_task')
        children =  data.split('\r\n')
        for child in children:
            ChildTask(name=child, task=task).save()
        return save

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'project_task/task_delete.html'

    def test_func(self):
        return check_project(self.request.user)

    success_url = reverse_lazy('projectman:list_task')


class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'project_task/task_detail.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev


#Vistas modelo Comment
@login_required
def comment_list_filter(request, pk):
    comment = Comment.objects.filter(task=pk)
    context = {'comment': comment}
    return render(request, 'project_task/comment_list_filter.html', context)


class CommentCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "project_task/comment_create.html"

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie

    success_url = reverse_lazy('projectman:list_comment')


class CommentList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Comment
    template_name = 'project_task/comment_list.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'project_task/comment_create.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie

    success_url = reverse_lazy('projectman:list_comment')


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'inclusion_tags/modal_eliminar.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev

    success_url   = reverse_lazy('projectman:list_comment')


class CommentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Comment
    template_name = 'project_task/comment_detail.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie


@login_required
def modalComment(request):
    return render(request, 'project_task/prueba_modal.html', {})


@login_required
def get_task_child(request, task_pk):
    task = Task.objects.get(id=task_pk)
    child = serializers.serialize('json', task.task_child.all())
    data = json.loads(child)
    return render(request, 'project_task/child_task_list.html', {'data': data, 'task': task})


class CTaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ChildTask
    template_name = 'inclusion_tags/modal_eliminar.html'
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        dev = check_dev(self.request.user)
        man = check_project(self.request.user)
        return dev or man


class CTaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ChildTask
    template_name = 'project_task/child_task_create.html'
    form_class = CTaskRegisterForm
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        dev = check_dev(self.request.user)
        man = check_project(self.request.user)
        return dev or man


class CTaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ChildTask
    template_name = 'project_task/child_task_create.html'
    form_class = CTaskRegisterForm
    success_url = reverse_lazy('projectman:list_task')

    def test_func(self):
        dev = check_dev(self.request.user)
        man = check_project(self.request.user)
        return dev or man

