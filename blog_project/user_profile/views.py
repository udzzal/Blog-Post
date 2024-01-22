from django.shortcuts import render,redirect,get_object_or_404
from .forms import registration_form,Login_from,User_profile_update_form,Update_profile_picture
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .decorator import login_not_required,not_need
from django.views.decorators.cache import never_cache
from .models import User
# Create your views here.

@never_cache
@not_need
def registration(request):
    fm=registration_form()
    if request.method == "POST":
        fm=registration_form(request.POST)
        
        if fm.is_valid():
            user=fm.save(commit=False)
            user.set_password(fm.cleaned_data.get('password'))
            user.save()
            messages.success(request,'sucessfully registration done')
            return redirect('login')
        
    context={
     "forms":fm
    }
    return render(request,"registration.html",context)


@never_cache
@not_need
def login_aut(request):
    fm=Login_from()
    if request.method == "POST":
        fm = Login_from(request.POST)
        if fm.is_valid():
            usern=fm.cleaned_data.get('username')
            passwor=fm.cleaned_data.get('password')
            useraut=authenticate(username=usern,password=passwor)
            if useraut:
                login(request,useraut)
                return redirect('registration')
            else:
                messages.warning(request,'wrong user') 
            
    context={
        "forms":fm
    }    
    return render(request,'login.html',context)    


def mylogout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request):
    account=get_object_or_404(User,pk=request.user.pk)
    form=User_profile_update_form(instance=account)
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect("home")
        form=User_profile_update_form(request.POST,instance=account)
        if form.is_valid():
            print(form.cleaned_data)  
            form.save()
            messages.success(request,"sucessfully save  ")
            return redirect("login")
        else:
            print(form.errors)    
    context={
        "account":account,
        "form":form,
    }        
    return render(request,"myprofile.html",context)        


@login_required(login_url='login')
def profile_picture(request):
    if request.method == "POST":
        fm=Update_profile_picture(request.POST,request.FILES)
        print(fm)
        if fm.is_valid():
            image=request.FILES['profile_image']
            user=get_object_or_404(User,pk=request.user.pk)
            
            if request.user.pk != user.pk:
                return redirect("login")
            user.profile_image=image
            user.save()
            messages.success(request,'profile picture updated')
        else:
            print(fm.errors)
    return redirect('profile')            
            
            
 

          
          
          