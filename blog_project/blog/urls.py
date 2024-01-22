from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.home,name='home'),
    path('blogs',views.blog,name='blog'),
    path('tag_blog/<str:slug>/',views.tag_blog,name='tag-blog'),
    path('catagory_blog/<str:slug>/',views.catagory_blog,name='catagory_blog'),
    path('blog_detail/<str:slug>/',views.blog_details,name='blog_details'),
    path('add_reply/<int:blog_id>/<int:comment_id>/',views.replay_comment,name='add_reply'),
    path('likeby_user/<int:pk>/',views.likeby_inblog,name='likeby_user'),
    path('sarch_blog',views.sarch_bar,name='sarch_blog'),
    path('myblog',views.myblog,name="myblog"),
    path('add_blog',views.add_blog,name='add_blog'),
    
]



