from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from store.models import Product, Variation
from django.shortcuts import get_object_or_404

class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

@api_view(['GET'])
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return Response({'cart_id': cart})


@api_view(['POST'])
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user).first()
            ex_var_list = list(cart_item.variations.all().values_list('id', flat=True))

            if product_variation == ex_var_list:
                # increase the cart item quantity
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                cart_item.variations.set(product_variation)
                cart_item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            cart_item.variations.set(product_variation)
            cart_item.save()

        return Response({'message': 'Cart item added successfully'})
    else:
        return Response({'message': 'User must be authenticated'})

@api_view(['POST'])
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        current_user = request.user
        if current_user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=current_user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return Response({'message': 'Cart item removed successfully'})
    except:
        return Response({'message': 'Failed to remove cart item'})

@api_view(['POST'])
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        current_user = request.user
        if current_user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=current_user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
        return Response({'message': 'Cart item removed successfully'})
    except:
        return Response({'message': 'Failed to remove cart item'})
