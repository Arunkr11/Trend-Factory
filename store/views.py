from django.shortcuts import render,redirect
from django.views.generic import View,DetailView,TemplateView
from store.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import Product,BasketItem,Size,Order,OrderItems

# Create your views here.

#url : localhost:8000/registration/
#method : POST and GET
#Form : RegistrationForm
class SignupView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request,'register.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        return render(request,'login.html',{'form':form})
    
#url : localhost:8000/login/
#method : POST and GET
#Form : LoginForm

class SigninView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            u_name = form.cleaned_data.get('username')
            psw = form.cleaned_data.get('password')
            user_object = authenticate(request,username=u_name, password=psw)
            if user_object:
                login(request,user_object)
                return redirect('index')
        messages.error(request,'Invalid credentials')
        return render(request,'login.html',{'form':form})
    
    
class IndexView(View):
    def get(self, request, *args, **kwargs):
        qs = Product.objects.all()
        return render(request,'index.html',{"data":qs})
    
class ProductDetailView(View):
    def get(self, request, *args,**kwargs):
        id = kwargs.get('pk')
        qs = Product.objects.get(id=id)
        return render(request,'product_detail.html',{"data":qs})
    
class HomeView(TemplateView):
    template_name = 'base.html'
    
class AddToBasketView(View):
    def post(self, request, *args, **kwargs):
        size = request.POST.get('size')
        size_obj = Size.objects.get(name=size)
        qty  = request.POST.get('qty')
        id   = kwargs.get('pk')
        product_obj = Product.objects.get(id=id)
        BasketItem.objects.create(
            size_object = size_obj,
            qty = qty,
            product_object = product_obj,
            basket_object = request.user.cart
        )
        return redirect('cart')
    
    
class BasketItemListView(View):
    def get(self, request, *args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_place=False)
        return render(request,'cart.html',{'data':qs})
    
    
class BasketItemRemoveView(View):
    def get(self, request, *args,**kwargs):
        id = kwargs.get('pk')
        basket_item_obj = BasketItem.objects.get(id=id)
        basket_item_obj.delete()
        return redirect('cart')
    
class CartItemUpdateqtyView(View):
    def post(self, request, *args,**kwargs):
        action = request.POST.get('CounterButton')
        id=kwargs.get('pk')
        basket_item_object = BasketItem.objects.get(id=id)
        if action == '+':
            basket_item_object.qty+=1
            basket_item_object.save()
        else:
            basket_item_object.qty-=1
            basket_item_object.save()
        print (action)
        return redirect('cart')
    
class CheckoutView(View):
    def get(self, request, *args,**kwargs):
        
        return render(request,'checkout.html')
    
    def post(self, request,*args,**kwargs):
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
    # order instance
        
        order_obj = Order.objects.create(
            user_object=request.user,
            delivery_address=address,
            phone=phone,
            email=email,
            total=request.user.cart.cart_total
        )
        
        # orderitem instance
        try:
            basket_items = request.user.cart.cart_item
            for bi in basket_items:
                OrderItems.objects.create(
                order_object=order_obj,
                basket_item_object=bi,
                
            )
                bi.is_order_place=True
                bi.save()
        except:
            order_obj.delete()
            
        finally:
            return redirect('index')
    
class Ordersummery(View):
    def get(self, request, *args,**kwargs):
        qs=OrderItems.objects.all()
        return render(request,'oredrsummery.html',{'data':qs})