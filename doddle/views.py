from django.shortcuts import render
from .serializers import *
from .models import *
from .serializers import *
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import *
# Create your views here.


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ALlUsers(viewsets.ModelViewSet):
    # serializer_class = UserSerializer
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', ]



# class RegisterApi(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#     def post(self, request, *args,  **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "message": "User Created Successfully.",
#         })



class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email = email)
            validate = check_password(password, user.password)
            if validate:
                token = str(RefreshToken.for_user(user))
                access = str(RefreshToken.for_user(user).access_token)
                return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "access": access,
                "refresh": token,

                })
            else:
                content = {"detail": "Password Do not Match"}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        except:
            content = {"detail": "No active account found with the given credentials"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)






