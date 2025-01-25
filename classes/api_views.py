from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status, response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from .models import Class
from courses.models import Course


# class list
class ClassListView(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = serializers.ClassListSerializer
    permission_classes = [AllowAny]

class MyClassListView(generics.ListAPIView):
    serializer_class = serializers.ClassListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        user = self.request.user
        return Class.objects.filter(students=user)

class ClassSearchView(generics.ListAPIView):
    serializer_class = serializers.ClassListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        key = self.kwargs['key']
        classes = Class.objects.filter(Q(title__contains=key))
        return classes

class MyClassSearchView(generics.ListAPIView):
    serializer_class = serializers.ClassListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        key = self.kwargs['key']
        user = self.request.user
        classes = Class.objects.filter(Q(title__contains=key), students=user)
        return classes

# class join
class JoinClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        class1 = get_object_or_404(Class, pk=class_id)
        
        password = request.data['password']
        if class1.password != str(password):
            return response.Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        if class1.students.filter(id=request.user.id).exists():
            return response.Response({"message": "You already joined thid class"}, status=status.HTTP_400_BAD_REQUEST)

        class1.students.add(request.user)
        return response.Response({"message": "You joined the class successfully"}, status=status.HTTP_200_OK)
    
# left class
class LeaveClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        class1 = get_object_or_404(Class, pk=class_id)

        if not class1.students.filter(id=request.user.id).exists():
            return response.Response({"message": "you havent joined in the class"}, statuts=status.HTTP_400_BAD_REQUEST)
    
        if class1.creator == request.user:
            return response.Response({"message": "The creator can't leave the class"}, status=status.HTTP_400_BAD_REQUEST)
        
        class1.students.remove(request.user)
        return response.Response({"message": "You left successfully"}, status=status.HTTP_200_OK)

# class detail
class ClassDetailView(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = serializers.ClassDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

# class create
class ClassCreateView(generics.CreateAPIView):
    queryset = Class
    serializer_class = serializers.ClassCreateSerializer
    permission_classes = [IsAuthenticated]

# clsas update
class ClassUpdateView(generics.UpdateAPIView):
    queryset = Class.objects.all()
    serializer_class = serializers.ClassUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        classes = self.get_object()
        if classes.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to update this class")
        serializer.save()

# class add course
class AddCourse(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id, course_id):
        classes = get_object_or_404(Class, pk=class_id)
        course = get_object_or_404(Course, pk=course_id)

        if classes.creator != request.user:
            return response.Response({"message": "You dont have access to this course"}, status=status.HTTP_403_FORBIDDEN)
        
        classes.courses.add(course)
        return response.Response({"message": "Course added to class successfully"}, status=status.HTTP_200_OK)
        

# class delete
class ClassDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        classes = get_object_or_404(Class, pk=self.kwargs['pk'])
        return classes

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to delete this class")
        
        instance.delete()