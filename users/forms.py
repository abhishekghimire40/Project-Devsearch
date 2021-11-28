from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Skill,Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
        labels = {'first_name': 'Name'}
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': "input"})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','username','email','short_intro','location','bio','profile_image','social_github','social_linkedin','social_twitter','social_website','social_facebook']

    def __init__(self, *args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': "input"})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields =['name','description']
        
    def __init__(self, *args, **kwargs):
        super(SkillForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': "input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['sender_name','email','subject','body']
        labels = {
            'sender_name': 'Name',
            'email':'Email',
            'subject':"Subject",
            'body':'Message'
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': "input"})