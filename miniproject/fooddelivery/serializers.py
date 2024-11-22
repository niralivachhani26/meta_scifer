from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Restaurant, MenuItem, Order, OrderItem, Delivery

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

        def create(self, validated_data):
            user = User.objects.create_user(
                username = validated_data['username'],
                email = validated_data['email'],
                password = validated_data['password'],
            )
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(**data)

        if user:
            return user
        raise serializers.ValidationError("Invalid username or password")

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many = True, read_only = True)

    class Meta:
        model = Restaurant
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    restaurant = RestaurantSerializer()

    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    menu_items = MenuItemSerializer(many=True, read_only=True)
    order = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Delivery
        fields = '__all__'