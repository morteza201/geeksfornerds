from rest_framework import serializers
from .models import Animation
from accounts.models import CustomUser

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

class AnimationListSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)
    class Meta:
        model = Animation
        fields = ['id', 'title', 'src', 'creator', 'created_at']

class AnimationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['id', 'title', 'src']
    
    def create(self, validated_data):
        animation = Animation.objects.create(
            title = validated_data['title'],
            src = validated_data['src'],
            creator = self.context['request'].user
        )

        return animation

class AnimationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['title', 'src']