from django.shortcuts import redirect
from store.models import BasketItem
from django.contrib import messages



def signin_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in")
            return redirect('signin')
        else:
            return fn(request, *args, **kwargs)
    return wrapper

def owner_permission(fn):
    def wrapper(request,*args, **kwargs):
        id =kwargs.get('pk')
        basket_item =BasketItem.objects.get(id=id)
        if basket_item.basket_object.owner != request.user:
            messages.error(request,'permission denied')
            return redirect('signin')
        else:
            return fn(request, *args, **kwargs)
    return wrapper