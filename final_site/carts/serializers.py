from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    sub_total = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['product', 'variations', 'quantity', 'is_active', 'sub_total']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['created_date', 'cart_id', 'cart_items']
        

