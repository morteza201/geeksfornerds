from rest_framework import serializers
from .models import CustomUser
from courses.serializers import CourseListSerializer
from roadmaps.serializers import RoadmapListSerializer
from rest_framework.validators import UniqueValidator

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, min_length=8, max_length=128)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=True
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        user = self.context['request'].user
        if CustomUser.objects.exclude(id=user.id).filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        if CustomUser.objects.exclude(id=user.id).filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        
        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.id != instance.id:
            raise serializers.ValidationError({"Authorize": "You dont have permisson for this user"})
        
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=128, min_length=8, required=True, write_only=True)
    new_password = serializers.CharField(max_length=128, min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(max_length=128, min_length=8, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords did'nt match."})
        
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "The old password is incorrect"})
        
        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = []

class UserViewSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True, read_only=True)
    roadmaps = RoadmapListSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'courses', 'roadmaps']
