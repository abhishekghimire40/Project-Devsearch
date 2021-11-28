from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm,ProfileForm,SkillForm,MessageForm
from .utils import searchProfiles,paginateProfiles


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            else:
                messages.error(request,"Username and password donot match.")
        except:
            messages.error(request,"Username doesn't exist.")


    return render(request,'users/login.html')


def logoutUser(request):
    logout(request)
    messages.success(request,"You have been successfully logged out!")
    return redirect('login')


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,"User was created successfully! ")
            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request,"An error has occurred. Please,try again.")


    context = {'page':page, 'form': form}
    return render(request,'users/login.html',context)




def profiles(request):
    profiles,text = searchProfiles(request)
    profiles,paginator = paginateProfiles(request,profiles,6)
    context = {'profiles':profiles,'text':text,'paginator':paginator}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description="")
    otherSkills = profile.skill_set.filter(description="")
    context = {"profile":profile,"topskill":topSkills,"otherSkills":otherSkills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile,'skills':skills,'projects':projects}
    return render(request,'users/account.html',context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method=='POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={'form':form }
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    page = "add"
    profile = request.user.profile
    form = SkillForm()
    if request.method =="POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner =  profile
            skill.save()
            return redirect('account')
    context={'form':form,'page':page}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def editSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    context ={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def deleteSkill(request,pk):
    profile = request.user.profile
    object = profile.skill_set.get(id=pk)
    if request.method == "POST":
        object.delete()
        return redirect('account')
    context = {'object':object}
    return render(request,'delete_template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    newmessageCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests,'newmessage':newmessageCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message1 = profile.messages.get(id=pk)
    if message1.is_read == False:
        message1.is_read = True
        message1.save() 
    context = {'message':message1}
    return render(request,'users/message.html',context)

def sendMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    print(recipient)
    form = MessageForm()
    if request.user.is_authenticated:
        sender = request.user.profile
    else:
        sender = None
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recepient = recipient
            if sender:
                message.sender_name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request,"Your message was sent successfully!")
            return redirect('user-profile',recipient.id)
    context ={'form':form,'recipient':recipient}
    return render(request,'users/message_form.html',context)