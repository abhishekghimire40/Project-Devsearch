from django.contrib.auth import login
from django.core import paginator
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages
from .models import Project,Tag
from .forms import ProjectForm,ReviewForm
from .utils import searchProjects,paginateProjects


def projects(request):
    projects,text = searchProjects(request)
    projects,paginator = paginateProjects(request,projects,6)
    
    context = {'projects': projects,'text':text,'paginator':paginator}
    return render(request,'projects/projects.html',context)

@login_required(login_url='login')
def project(request,pk):  
    projectObj = Project.objects.get(id=pk) 
    reviews  = projectObj.review_set.all()
    form = ReviewForm()
    if request.method == "POST":
        profile = request.user.profile
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = profile
            review.save()
            projectObj.getVotecount
            messages.success(request,"Your review has been posted successfully.")
            return redirect('project',pk=projectObj.id)
    context = {'project':projectObj,'form':form,'reviews':reviews}
    return render(request,'projects/single-project.html',context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == "POST":
        newtags = request.POST.get("newtags")
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    form = ProjectForm(instance=project)
    if request.method == "POST":
        newtags = request.POST.get("newtags").replace(","," ").split()
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form':form,'project':project}
    return render(request,'projects/project_form.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('account')
    context = {'object':project}
    return render(request,'delete_template.html',context)