from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.AnimationListView.as_view(), name='animations_list'),
    path('search/<str:key>/', api_views.AnimationSearchView.as_view(), name='animations_search'),
    path('create/', api_views.AnimationCreateView.as_view(), name='animations_create'),
    path('<int:pk>/update/', api_views.AnimationUpdateView.as_view(), name='animations_edit'),
    path('<int:pk>/delete/', api_views.AnimationDeleteView.as_view(), name='animations_delete'),
]