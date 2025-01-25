from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.RoadmapListView.as_view(), name='roadmaps_list'),
    path('my-roadmaps/', api_views.RoadmapListView.as_view(), name='user_roadmaps_list'),
    path('<int:pk>/', api_views.RoadmapDetailView.as_view(), name='roadmaps_detail'),
    path('search/<str:key>/', api_views.RoadmapSearchView.as_view(), name='roadmaps_search'),
    path('search-my/<str:key>/', api_views.MyRoadmapSearchView.as_view(), name='user_roadmaps_search'),
    path('create/', api_views.RoadmapCreateView.as_view(), name='roadmaps_create'),
    path('update/<int:pk>/', api_views.RoadmapUpdateView.as_view(), name='roadmaps_update'), 
    path('delete/<int:pk>/', api_views.RoadmapDeleteView.as_view(), name='roadmaps_delete'),
    path('steps-<int:pk>/search/<str:key>/', api_views.StepSearchView.as_view(), name='roadmaps_steps_search'),
    path('steps-<int:pk>/', api_views.StepListView.as_view(), name='roadmaps_steps_list'),
    path('steps/<int:pk>/', api_views.StepDetailView.as_view(), name='roadmaps_steps_detail'),
    path('steps-<int:pk>/create/', api_views.StepCreateView.as_view(), name='roadmaps_steps_create'),
    path('steps-<int:pk>/update/', api_views.StepUpdateView.as_view(), name='roadmaps_steps_update'), 
    path('steps-<int:pk>/delete/', api_views.StepDeleteView.as_view(), name='roadmaps_steps_delete'),
    path('comments/create/', api_views.CommentCreateView.as_view(), name='roadmaps_comments_create'),
    path('comments/delete/<int:pk>/', api_views.CommentDeleteView.as_view(), name='roadmaps_comments_delete'),
    path('rate-<int:pk>/', api_views.RateCreateView.as_view(), name='roadmaps_vote_rating'),    
]