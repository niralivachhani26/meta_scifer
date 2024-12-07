from django.urls import path,include
from . import views

urlpatterns = [
    path('index/',views.index, name = 'index'),
    path('menu_list/',views.menu_list, name = 'menu_list'),
    path('contact/',views.contact, name = 'contact'),
    path('about/',views.about, name = 'about'),
    path('thanks/<int:order_id>',views.thanks, name = 'thanks'),
    path('cart/',views.cart, name = 'cart'),
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:food_id>/ajax', views.update_cart, name='update_cart'),
    path('remove_cart/<int:food_id>', views.remove_from_cart, name='remove_cart'),
]