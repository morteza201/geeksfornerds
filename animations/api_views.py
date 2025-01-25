from . import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Animation

class AnimationListView(generics.ListAPIView):
    serializer_class = serializers.AnimationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        animations = Animation.objects.filter(creator=self.request.user)
        return animations

class AnimationSearchView(generics.ListAPIView):
    serializer_class = serializers.AnimationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        key = self.kwargs['key']
        animatinos = Animation.objects.filter(Q(title__contains=key), creator=self.request.user)
        return animatinos

class AnimationCreateView(generics.CreateAPIView):
    queryset = Animation
    serializer_class = serializers.AnimationCreateSerializer
    permission_classes = [IsAuthenticated]

class AnimationUpdateView(generics.UpdateAPIView):
    queryset = Animation.objects.all()
    serializer_class = serializers.AnimationUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        animation = self.get_object()
        if animation.creator != self.request.user:
            return PermissionDenied("You dont have access to update this animation")
        serializer.save()

class AnimationDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        animation = get_object_or_404(Animation, pk=self.kwargs['pk'])
        return animation

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("You dont have permisson to delete this animation")
        
        instance.delete()