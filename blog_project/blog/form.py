from django import forms
from .models import Blog


class Comment_form(forms.Form):
    text=forms.CharField(widget=forms.Textarea,required=True)
    
    
class Addblog_Form(forms.ModelForm):
    
    class Meta:
        model =Blog
        fields = ('titel','catagory','banner','description','tags')

