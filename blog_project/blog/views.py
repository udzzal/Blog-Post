from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from .models import (
    Blog,
    Catagory,
    Tag,
    Comment,
    Replay,
)
from django.utils.text import slugify
from user_profile.models import User
from .form import Comment_form,Addblog_Form
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    blo=Blog.objects.order_by('created_date')
    tags=Tag.objects.order_by('created_date')
    context={
        "blogs" :blo,
        "tag":tags
    }
    return render(request,'home.html',context)

def blog(request):
    
    blo=Blog.objects.order_by('created_date')
    tags=Tag.objects.order_by('created_date')
    paginator=Paginator(blo,2,orphans=1)
    page_number=request.GET.get('page',1)
    
    try:
        bloger=paginator.page(page_number)
    except PageNotAnInteger:
        bloger=paginator.page(1)   
    except EmptyPage:
        bloger=paginator.page(1)

    context={
        "blogs" :bloger,
        "tag":tags,
    }
    return render(request,'blog.html',context)

def catagory_blog(request,slug):
    catagory=get_object_or_404(Catagory,slug=slug)
    queryset=catagory.catagory_blog.all()
    tag=Tag.objects.order_by('created_date')[:5]
    
    paginator=Paginator(queryset,2)
    page_number=request.GET.get('page',1)
    allblogs=Blog.objects.order_by('created_date')[:3]
    try:
        blogs=paginator.page(page_number)
    except PageNotAnInteger:
        blogs=paginator.page(1)
    except EmptyPage:
        blogs=paginator.page(1)
            
    context={
        "blogs":blogs,
        "tag":tag,
        "all_blog":allblogs,
    }
    return render(request,"catagory_blog.html", context)

def tag_blog(request,slug):
    ttag=get_object_or_404(Tag,slug=slug)
    queryset=ttag.tag_blog.all()
    tag=Tag.objects.order_by('created_date')[:5]
    
    paginator=Paginator(queryset,2)
    page_number=request.GET.get('page',1)
    allblogs=Blog.objects.order_by('created_date')[:3]
    try:
        blogs=paginator.page(page_number)
    except PageNotAnInteger:
        blogs=paginator.page(1)
    except EmptyPage:
        blogs=paginator.page(1)
            
    context={
        "blogs":blogs,
        "tag":tag,
        "all_blog":allblogs
    }
    return render(request,'tag_blog.html',context)


def blog_details(request,slug):
    bloger=get_object_or_404(Blog,slug=slug )
    tags=Tag.objects.order_by('created_date')[:5]
    catagory=Catagory.objects.get(id=bloger.catagory.id)
    related_catagory=catagory.catagory_blog.all()
    like_by=request.user in bloger.likes.all()
    form=Comment_form()
    
    if request.method == "POST" and request.user.is_authenticated:
        form=Comment_form(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                blog=bloger,
                text=form.cleaned_data.get('text'),
            )
            return redirect('blog_details',slug=slug)
        
    context={
        "blog":bloger,
        "tag":tags,
        "recatagory":related_catagory,
        "form":form,
        "like_by":like_by,
    }
    return render(request,'blog_details.html',context)

@login_required(login_url="login")
def replay_comment(request,blog_id,comment_id):
    blog=get_object_or_404(Blog,id=blog_id)
    if request.method == "POST":
        form=Comment_form(request.POST)
        if form.is_valid():
            comment=get_object_or_404(Comment,id=comment_id)
            Replay.objects.create(
                user=request.user,
                text=form.cleaned_data.get('text'),
                comment=comment,
            )
    return redirect('blog_details',slug=blog.slug)

@login_required(login_url="login")
def likeby_inblog(request,pk):
    context={}
    blog=get_object_or_404(Blog,pk=pk)
    if request.user in blog.likes.all() :
        blog.likes.remove(request.user)
        context['likes']=False
        context['likes_count']=blog.likes.all().count()
        
    else:
        blog.likes.add(request.user)
        context['likes']=True
        context['likes_count']=blog.likes.all().count()
                                    
    return JsonResponse(context,safe=False) 


def sarch_bar(request):
    sarch_by=request.GET.get('sarch',None)
    bloger=Blog.objects.order_by("created_date")
    tags=Tag.objects.order_by('created_date')
    if sarch_by:
        blogs=Blog.objects.filter(
            Q(titel__icontains=sarch_by)|
            Q(catagory__titel__contains=sarch_by)|
            Q(user__username__contains=sarch_by)|
            Q(tags__titel__contains=sarch_by)
            
        ).distinct()
        context={
            "blogs":blogs,
            "bloger":bloger,
            "tag":tags,
        }
        return render(request,"sarch.html",context)
    else:                      
        return redirect("home")    
    
    
    
@login_required(login_url='login')            
def myblog(request):
    user=request.user.user_blog.all()
    paginator=Paginator(user,2)
    page=request.GET.get('page',1)
    
    
    try:
        blog=paginator.page(page)
    except PageNotAnInteger:
        blog=Paginator.page(1)
    except EmptyPage:
        blog=Paginator.page(1)
          
    context={
        "blogs":blog,
        "paginator":paginator,
    }
    return render(request,'myblog.html',context) 


def add_blog(request):
    form = Addblog_Form()

    if request.method == "POST":
        form = Addblog_Form(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['mtags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Catagory, pk=request.POST['catagory'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Blog added successfully")
            return redirect('blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context = {
        "form": form
    }
    return render(request,"add_blog.html",context)





