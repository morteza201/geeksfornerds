from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status, response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from .models import Roadmap, Step, Comment, Rate


class RoadmapListView(generics.ListAPIView):
    queryset = Roadmap.objects.all()
    serializer_class = serializers.RoadmapListSerializer
    permission_classes = [AllowAny]

class MyRoadmapListView(generics.ListAPIView):
    serializer_class = serializers.RoadmapListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        roadmaps = Roadmap.objects.filter(students=user)
        return roadmaps

class RoadmapSearchView(generics.ListAPIView):
    serializer_class = serializers.RoadmapListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        key = self.kwargs['key']
        roadmaps = Roadmap.objects.filter(Q(title__contains=key) | Q(description__contains=key))

        return roadmaps

class MyRoadmapSearchView(generics.ListAPIView):
    serializer_class = serializers.RoadmapListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        key = self.kwargs['key']
        user = self.request.user
        roadmaps = Roadmap.objects.filter(Q(title__contains=key) | Q(description__contains=key), students=user)

        return roadmaps

class RoadmapDetailView(generics.RetrieveAPIView):
    queryset = Roadmap.objects.all()
    serializer_class = serializers.RoadmapDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

class RoadmapCreateView(generics.CreateAPIView):
    queryset = Roadmap
    serializer_class = serializers.RoadmapCreateSerializer
    permission_classes = [IsAuthenticated]

class RoadmapUpdateView(generics.UpdateAPIView):
    queryset = Roadmap.objects.all()
    serializer_class = serializers.RoadmapUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        roadmap = self.get_object()
        if roadmap.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to update this roadmap")
        serializer.save()

class RoadmapDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        roadmap = get_object_or_404(Roadmap, pk=self.kwargs['pk'])
        return roadmap

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to delete this roadmap")
        
        instance.delete()

class StepListView(generics.ListAPIView):
    serializer_class = serializers.StepListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        roadmap = get_object_or_404(Roadmap, pk=self.kwargs['pk'])
        steps = Step.objects.filter(roadmap=roadmap)
    
        return steps

class StepSearchView(generics.ListAPIView):
    serializer_class = serializers.StepListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        key = self.kwargs['key']
        roadmap = get_object_or_404(Roadmap, pk=self.kwargs['pk'])
        steps = Step.objects.filter(roadmap=roadmap)
        steps = steps.filter(Q(title__contains=key) | Q(description__contains=key))

        return steps

class StepDetailView(generics.RetrieveAPIView):
    queryset = Step.objects.all()
    serializer_class = serializers.StepDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class StepCreateView(generics.CreateAPIView):
    queryset = Step
    serializer_class = serializers.StepCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        roadmap = get_object_or_404(Roadmap, pk=self.kwargs['pk'])

        if roadmap.creator != self.request.user:
            return PermissionDenied("You dont have permission to create step for this roadmap")
        
        serializer.save(roadmap=roadmap)

class StepUpdateView(generics.UpdateAPIView):
    queryset = Step.objects.all()
    serializer_class = serializers.StepUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        step = self.get_object()
        if step.roadmap.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to update this step")
        serializer.save()

class StepDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        step = get_object_or_404(Step, pk=self.kwargs['pk'])
        return step

    def perform_destroy(self, instance):
        if instance.roadmap.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to delete this step")
        
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
        roadmap = get_object_or_404(Roadmap, pk=self.kwargs['pk'])
        rate = Rate.objects.filter(creator=request.user, roadmap=roadmap)
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
                roadmap = roadmap
            )
        return response.Response({"message": "Rate voted successfully"}, status=status.HTTP_201_CREATED)