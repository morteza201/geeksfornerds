from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import ChangePasswordSerializer, UserCreateSerializer, UserUpdateSerializer, UserDeleteSerializer, UserViewSerializer

class GetUsernameView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        username = request.user.username
        return Response({"username": username}, status=status.HTTP_200_OK)

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserUpdateProfile(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserViewSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'