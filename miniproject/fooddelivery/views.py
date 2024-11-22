from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .models import Restaurant, MenuItem, Order, OrderItem, Delivery
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer, DeliverySerializer, \
    RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



def index(request):
    food_items = MenuItem.objects.order_by('-id')[:3]
    return render(request, 'home.html',{'food_items':food_items})

def menu_list(request):
    food_items = MenuItem.objects.all()
    return render(request, 'menu.html',{'food_items':food_items})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

@login_required
def thanks(request,order_id):
    order = get_object_or_404(Order, user=request.user, id =order_id)
    order.status = "Delivered"
    order.save()
    return render(request, 'thanks.html')

@login_required
def add_to_cart(request, food_id):
    food_item = get_object_or_404(MenuItem, id= food_id)
    restaurant = get_object_or_404(Restaurant, id = food_item.restaurant_id)
    order, created = Order.objects.get_or_create(user = request.user, restaurant = restaurant, status= 'Pending')

    order_item, created = OrderItem.objects.get_or_create(order = order,menu_item = food_item, price_per_item = food_item.price)

    if not created:
        order_item.quantity += 1
        order_item.save()
        
    messages.success(request, f"{food_item.name} added to cart!")
    return redirect('cart')

@login_required
def cart(request):
    user = request.user
    order = Order.objects.filter(user = user, status = "Pending").first()
    order_items = order.order_items.all() if order else []
    total = sum(item.total_price for item in order_items)
    order_id = order.id
    return render(request, 'cart.html',{'food_items' : order_items, 'total': total, 'order_id' : order_id})

@login_required
@csrf_exempt
def update_cart(request, food_id):
    order_item = get_object_or_404(OrderItem, id = food_id, order__user = request.user)
    price = 0

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            order_item.quantity = quantity
            order_item.save()
            messages.success(request, "Cart Updated!")

        price = quantity * order_item.price_per_item
    return JsonResponse({'success':True, 'price':price, 'per_item':order_item.price_per_item}, status = 200)

@login_required
def remove_from_cart(request, food_id):
    order_item = get_object_or_404(OrderItem, id = food_id, order__user = request.user)
    order_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart')


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = MenuItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


# Create your views here.
