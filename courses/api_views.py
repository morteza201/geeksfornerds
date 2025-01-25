from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status, response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from .models import Course, Lesson, Comment, Rate

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseListSerializer
    permission_classes = [AllowAny]

class MyCourseListView(generics.ListAPIView):
    serializer_class = serializers.CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.filter(students=user)
        return courses


class CourseSearchView(generics.ListAPIView):
    serializer_class = serializers.CourseListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        key = self.kwargs['key']
        courses = Course.objects.filter(Q(title__contains=key) | Q(description__contains=key))
        return courses

class MyCourseSearchView(generics.ListAPIView):
    serializer_class = serializers.CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        key = self.kwargs['key']
        user = self.request.user
        courses = Course.objects.filter(Q(title__contains=key) | Q(description__contains=key), students=user)
        return courses

class EnrollCourse(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        
        if course.students.filter(id=request.user.id).exists():
            return response.Response({"message": "You already enrolled thid course"}, status=status.HTTP_400_BAD_REQUEST)

        course.students.add(request.user)
        return response.Response({"message": "You enrolled the course successfully"}, status=status.HTTP_200_OK)

class IsEnrolled(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        if course.students.filter(id=request.user.id).exists():
            return response.Response({"message": True})
        return response.Response({"message": False})

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'
    

class CourseCreateView(generics.CreateAPIView):
    queryset = Course
    serializer_class = serializers.CourseCreateSerializer
    permission_classes = [IsAuthenticated]

class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        course = self.get_object()
        if course.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to update this course")
        serializer.save()
    
class CourseDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return course

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to delete this course")
        
        instance.delete()


class LessonListView(generics.ListAPIView):
    serializer_class = serializers.LessonListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        lessons = Lesson.objects.filter(course=course)
    
        return lessons

class LessonSearchView(generics.ListAPIView):
    serializer_class = serializers.LessonListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        key = self.kwargs['key']
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        lessons = lessons.filter(course=course)
        lessons = Lesson.objects.filter(Q(title__contatins=key) | Q(content__contains=key))
        return lessons

class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson
    serializer_class = serializers.LessonCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])

        if course.creator != self.request.user:
            return PermissionDenied("You dont have permission to create lesson for this course")
        
        serializer.save(course=course)

class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        lesson = self.get_object()
        if lesson.course.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to update this lesson")
        serializer.save()

class LessonDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        return lesson

    def perform_destroy(self, instance):
        if instance.course.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to delete this course")
        
        instance.delete()

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return comment
    
    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            return PermissionDenied("You dont have permisson to delete this comment")
        
        instance.delete()

class RateCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        rate = Rate.objects.filter(creator=request.user, course=course)
        rating = request.data.get('rating')

        if not rating or rating < 1 or rating > 5:
            return response.Response({"error": "Rating must be an integer between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)


        if rate.exists():
            rate = rate[0]
            rate.rating = rating
            rate.save()

        else:
            rate = Rate.objects.create(
                rating = int(rating),
                creator = self.request.user,
                course = course
            )
        return response.Response({"message": "Rate voted successfully"}, status=status.HTTP_201_CREATED)