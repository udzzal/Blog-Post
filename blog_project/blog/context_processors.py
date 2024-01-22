from .models import Catagory


def common_context(request):
    catagorys=Catagory.objects.all()
    
    context={
        "catagory" : catagorys,
    }
    return context
    
    