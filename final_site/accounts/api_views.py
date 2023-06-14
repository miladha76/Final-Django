from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from orders.models import Order

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileEditAPIView(APIView):
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    def get(self, request, format=None):
        userprofile = self.get_object()
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        userprofile = self.get_object()
        serializer = UserProfileSerializer(userprofile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboardd(request):
    orders = Order.objects.order_by('-created_at').filter(user=request.user, is_ordered=True)
    orders_count = orders.count()
    user_profile = UserProfile.objects.get(user=request.user)

    serializer = UserProfileSerializer(user_profile)
    context = {
        'orders_count': orders_count,
        'userprofile': serializer.data,
    }
    return Response(context)
