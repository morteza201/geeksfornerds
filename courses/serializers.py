from rest_framework import serializers
from .models import Course, Lesson, Comment
from accounts.models import CustomUser
from animations.models import Animation

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

class CommentListSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'creator', 'replied_comment', 'created_at']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'course', 'replied_comment']
    
    def validate(self, data):
        replied_comment = data.get('replied_comment')
        course = data.get('course')

        if replied_comment:
            if replied_comment.course != course:
                raise serializers.ValidationError("The parent comment does not exist.")
        
        return data 
    
    def create(self, validated_data):
        comment = Comment.objects.create(
            text = validated_data['text'],
            creator = self.context['request'].user,
            course = validated_data['course'],
            replied_comment = validated_data['replied_comment']
        )
        return comment

class CourseListSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'creator', 'get_rating', 'created_at', 'last_update']

class LessonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'animations', 'created_at']

class CourseDetailSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)
    comments = CommentListSerializer(read_only=True, many=True)
    lessons = LessonInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons', 'creator', 'get_rating', 'comments', 'created_at', 'last_update']

class AnimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['title', 'src']
    

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description']
    

    def create(self, validated_data):
        course = Course.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            creator = self.context['request'].user
        )
        course.save()

        return course

class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description']


class LessonListSerializer(serializers.ModelSerializer):
    animations = AnimationSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course', 'animations', 'created_at']

class CourseInfoSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'creator']

class LessonDetailSerializer(serializers.ModelSerializer):
    course = CourseInfoSerializer(read_only=True)
    animations = AnimationSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course', 'animations', 'created_at']

class LessonCreateSerializer(serializers.ModelSerializer):
    animations = serializers.PrimaryKeyRelatedField(queryset=Animation.objects.all(), many=True)

    class Meta:
        model = Lesson
        fields = ['title', 'content', 'animations']
    
    def create(self, validated_data):
        lesson = Lesson.objects.create(
            title = validated_data['title'],
            content = validated_data['content'],
            course = validated_data['course'],
        )
        for animation in validated_data['animations']:
            lesson.animations.add(animation);
        return lesson

class LessonUpdateSerializer(serializers.ModelSerializer):

    animations = serializers.PrimaryKeyRelatedField(queryset=Animation.objects.all(), many=True)
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'animations']