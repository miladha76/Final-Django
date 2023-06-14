from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PaymentSerializer, OrderSerializer
from .models import Order, Payment, OrderItem
from carts.models import *
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .forms import *
from rest_framework import status
from datetime import date
from carts.serializers import CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
@api_view(['POST'])
def payments(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=serializer.validated_data['orderID'])
        payment = Payment(
            user=request.user,
            payment_id=serializer.validated_data[''],
            payment_method=serializer.validated_data['payment_method'],
            amount_paid=order.order_total,
            status=serializer.validated_data['status']
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        # Move the cart items to Order Product table and update product stock
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True
            )
            order_item.variations.set(item.variations.all())
            order_item.save()
            item.product.stock -= item.quantity
            item.product.save()
        cart_items.delete()
        data = {
            'order_number': order.order_number,
           
        }
        return Response(data)
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    total = 0
    quantity = 0
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    data = {
        'user': current_user.id,
        'first_name': request.data.get('first_name'),
        'last_name': request.data.get('last_name'),
        'phone': request.data.get('phone'),
        'email': request.data.get('email'),
        'address_line_1': request.data.get('address_line_1'),
        'address_line_2': request.data.get('address_line_2'),
        'country': request.data.get('country'),
        'city': request.data.get('city'),
        'order_note': request.data.get('order_note'),
        'order_total': grand_total,
        'tax': tax,
        'ip': request.META.get('REMOTE_ADDR')
    }

    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        order = serializer.save()
        yr = date.today().strftime('%Y')
        dt = date.today().strftime('%d')
        mt = date.today().strftime('%m')
        d = date(int(yr), int(mt), int(dt))
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.save()

       
        cart_items = CartItem.objects.filter(user=current_user)
        serializer = CartItemSerializer(cart_items, many=True)

        context = {
            'order': order,
            'cart_items': serializer.data,
            'total': total,
            'tax': tax,
            'grand_total': grand_total
        }
        return Response(context, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderItem.objects.filter(order=order)

        subtotal = sum(item.product_price * item.quantity for item in ordered_products)

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'payment': payment,
            'subtotal': subtotal
        }
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return Response({'detail': 'Order or Payment not found.'}, status=404)
