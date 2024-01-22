from django.urls import path
from . import views



urlpatterns = [
    
    
    path('login',views.login_aut,name="login"),
    path('registration',views.registration,name="registration"),
    path('logout',views.mylogout,name="logout"),
    path('profile',views.profile,name='profile'),
    path('profile_updated',views.profile_picture,name='profile_updated'),
    
    
    
]




