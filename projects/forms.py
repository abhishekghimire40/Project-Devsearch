from django import forms
from django.db.models.base import Model
from django.forms import ModelForm, fields
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','featured_image','demo_link','source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }

    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        
        #if we want to style fields differently then we can do like this:-
        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add title'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels ={
            'value':'Vote',
            'body':'Comment'
        }


    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})