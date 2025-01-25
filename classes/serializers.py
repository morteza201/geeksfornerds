from rest_framework import serializers
from accounts.models import CustomUser
from .models import Class
from courses.models import Course
from courses.serializers import CourseInfoSerializer

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']
        
class ClassListSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'title', 'description', 'creator', 'created_at']

class ClassDetailSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)
    courses = CourseInfoSerializer(read_only=True, many=True)


    class Meta:
        model = Class
        fields = ['id', 'title', 'description', 'creator', 'courses', 'created_at']

class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['title', 'description', 'password']
    

    def create(self, validated_data):
        classes = Class.objects.create(
            title = validated_data['title'],
            password = validated_data['password'],
            creator = self.context['request'].user
        )
        classes.students.add(self.context['request'].user)
        classes.save()

        return classes

class ClassUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['title', 'description', 'password']