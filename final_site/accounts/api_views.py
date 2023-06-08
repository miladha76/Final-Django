from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets

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
