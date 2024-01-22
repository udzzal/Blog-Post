from django.shortcuts import redirect

def login_not_required(view_function):
    
    def wrapper(request, *args, **kwargs):
       
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to home if logged in
        else:
            return view_function(request, *args, **kwargs)  # Call original view if not logged in

    return wrapper 
        
def not_need(view_function):
    
    def wrap(request,*args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect('home')  
        else:
            return view_function(request,*args, **kwargs)
        
    return wrap
    
    