from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.ClassListView.as_view(), name='classes_list'),
    path('my-classes/', api_views.MyClassListView.as_view(), name='user_classes_list'),
    path('<int:pk>/', api_views.ClassDetailView.as_view(), name='classes_detail'),
    path('search/<str:key>/', api_views.ClassSearchView.as_view(), name='classes_search'),
    path('search-my/<str:key>/', api_views.MyClassSearchView.as_view(), name='user_classes_search'),
    path('join/<int:class_id>/', api_views.JoinClass.as_view(), name='classes_join'),
    path('leave/<int:class_id>/', api_views.LeaveClass.as_view(), name='classes_leave'),
    path('create/', api_views.ClassCreateView.as_view(), name='classes_create'),
    path('update/<int:pk>/', api_views.ClassUpdateView.as_view(), name='classes_update'),
    path('add/<int:class_id>/<int:course_id>/', api_views.AddCourse.as_view(), name='classes_add_course'),
    path('delete/<int:pk>/', api_views.ClassDeleteView.as_view(), name='classes_delete'),
]