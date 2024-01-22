
from django import forms
from .models import User


#//  start your from...

class Login_from(forms.Form):
    username=forms.CharField( max_length=200, required=True)
    password=forms.CharField( max_length=200, required=True,widget=forms.PasswordInput)


#// registration from 
class registration_form(forms.ModelForm):
    
    class Meta:
        model=User
        fields=('username','email','password')
        
    def clean_username(self):
        username=self.cleaned_data.get("username")
        model=self.Meta.model
        user=model.objects.filter(username__iexact=username)
        if user.exists():
            raise forms.ValidationError('A user already has this name')
        
        return self.cleaned_data.get('username')
    
    def clean_email(self):
        email=self.cleaned_data.get("email")
        model=self.Meta.model
        user=model.objects.filter(email__iexact=email)
        if user.exists():
            raise forms.ValidationError('A user already has this email')
        
        return self.cleaned_data.get('email')
    
    def clean_password(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.data.get('re-password')
        
        if password != confirm_password:
            raise forms.ValidationError('password does not match')
        
        return self.cleaned_data.get('password')
    
    
    #// user profile update file 
    
class User_profile_update_form(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    class Meta:
        model=User
        fields=('first_name','last_name','username','email')
        
    def clean_username(self):
        username=self.cleaned_data.get("username")
        model=self.Meta.model
        user=model.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        if user.exists():
            raise forms.ValidationError('A user already has this name')
        
        return self.cleaned_data.get('username')
    
    def clean_email(self):
        email=self.cleaned_data.get("email")
        model=self.Meta.model
        user=model.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if user.exists():
            raise forms.ValidationError('A user already has this email')
        
        return self.cleaned_data.get('email')
    
    def change_password(self):
        pass1 = self.data['password']
        pass2 = self.data['new-password']
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('password didn"t match')
        else:
            self.instance.set_password(pass2)
            self.instance.save()
            
    def clean(self):
        self.change_password()    
            

class Update_profile_picture(forms.Form):
    profile_image=forms.ImageField(required=True)
    
    
