from rest_framework import serializers
from accounts.models import CustomUser
from .models import Roadmap, Step, Comment, Rate


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
        fields = ['text', 'roadmap', 'replied_comment']
    
    def validate(self, data):
        replied_comment = data.get('replied_comment')
        roadmap = data.get('roadmap')

        if replied_comment:
            if replied_comment.roadmap != roadmap:
                raise serializers.ValidationError("The parent comment does not exist.")
        
        return data 
    
    def create(self, validated_data):
        comment = Comment.objects.create(
            text = validated_data['text'],
            creator = self.context['request'].user,
            roadmap = validated_data['roadmap'],
            replied_comment = validated_data['replied_comment'] 
        )
        return comment

class StepInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['title', 'description']

class RoadmapListSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)

    class Meta:
        model = Roadmap
        fields = ['id', 'title', 'description', 'creator', 'get_rating', 'created_at', 'last_update']

class RoadmapDetailSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)
    comments = CommentListSerializer(read_only=True, many=True)
    steps = StepInfoSerializer(read_only=True, many=True)


    class Meta:
        model = Roadmap
        fields = ['id', 'title', 'description', 'steps', 'creator', 'get_rating', 'comments', 'created_at', 'last_update']

class RoadmapCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = ['title', 'description']
    

    def create(self, validated_data):
        roadmap = Roadmap.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            creator = self.context['request'].user
        )
        roadmap.save()

        return roadmap

class RoadmapUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = ['title', 'description']

class StepListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'title', 'description', 'roadmap', 'created_at']

class RoadmapInfoSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(read_only=True)

    class Meta:
        model = Roadmap
        fields = ['id', 'title', 'description', 'creator']

class StepDetailSerializer(serializers.ModelSerializer):
    roadmap = RoadmapInfoSerializer(read_only=True)

    class Meta:
        model = Step
        fields = ['id', 'title', 'description', 'roadmap', 'created_at']

class StepCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['title', 'description']
    
    def create(self, validated_data):
        step = Step.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            roadmap = validated_data['roadmap'],
        )

        return step

class StepUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Step
        fields = ['title', 'description']