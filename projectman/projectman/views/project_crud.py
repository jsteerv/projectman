from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ..forms import ProjectForm
from ..models import Project
from .login import check_project, check_client


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


@login_required
def project_list_filter(request, pk):
    projects = Project.objects.filter(client=pk)
    context = {'projects': projects}
    print(pk)
    return render(request, 'project_task/project_list_filter.html', context)


@login_required
def project_moveup(request, pk):
    project = get_object_or_404(Project, pk=pk)
    lista = Project.objects.all()
    x = [e for e in lista if e.position == (project.position+1)]
    if len(x)>0:
        project.position = x[0].position
        x[0].position = x[0].position-1
        project.save()
        x[0].save()
    print(Project.objects.all())
    return redirect('/list/project/')


@login_required
def project_movedown(request, pk):
    project = get_object_or_404(Project, pk=pk)
    lista = Project.objects.all()
    x = [e for e in lista if e.position == (project.position - 1)]
    if len(x)>0:
        project.position = x[0].position
        x[0].position = x[0].position+1
        project.save()
        x[0].save()
    print(x)
    print(x)
    return redirect('/list/project/')
