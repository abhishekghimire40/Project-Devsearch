from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from .models import Profile,Skill


def paginateProfiles(request,profiles,results):
    page = request.GET.get('page')
    paginator = Paginator(profiles,results,orphans=2)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    return profiles,paginator

def searchProfiles(request):
    text = ""
    if request.GET.get('text'):
        text = request.GET.get('text')

    skills = Skill.objects.filter(name__icontains=text)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=text) |
        Q(short_intro__icontains=text) |
        Q(skill__in=skills)
        )
    return profiles,text