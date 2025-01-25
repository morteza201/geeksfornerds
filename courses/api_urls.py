from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.CourseListView.as_view(), name='courses_list'),
    path('my-courses/', api_views.MyCourseListView.as_view(), name='user_courses_list'),
    path('<int:pk>/', api_views.CourseDetailView.as_view(), name='courses_detail'),
    path('search/<str:key>/', api_views.CourseSearchView.as_view(), name='courses_search'),
    path('search-my/<str:key>/', api_views.MyCourseSearchView.as_view(), name='user_courses_search'),
    path('create/', api_views.CourseCreateView.as_view(), name='courses_create'),
    path('enroll/<int:course_id>/', api_views.EnrollCourse.as_view(), name='courses_enroll'),
    path('enrolled/<int:course_id>/', api_views.IsEnrolled.as_view(), name='courses_is_enrolled'),
    path('update/<int:pk>/', api_views.CourseUpdateView.as_view(), name='courses_update'), 
    path('delete/<int:pk>/', api_views.CourseDeleteView.as_view(), name='courses_delete'),
    path('lessons-<int:pk>/', api_views.LessonListView.as_view(), name='courses_lessons_list'),
    path('lessons-<int:pk>/search/<str:key>/', api_views.LessonSearchView.as_view(), name='courses_lessons_search'),
    path('lessons/<int:pk>/', api_views.LessonDetailView.as_view(), name='courses_lessons_detail'),
    path('lessons-<int:pk>/create/', api_views.LessonCreateView.as_view(), name='courses_lessons_create'),
    path('lessons-<int:pk>/update/', api_views.LessonUpdateView.as_view(), name='courses_lessons_update'), 
    path('lessons-<int:pk>/delete/', api_views.LessonDeleteView.as_view(), name='courses_lessons_delete'),
    path('comments/create/', api_views.CommentCreateView.as_view(), name='courses_comments_create'),
    path('comments/delete/<int:pk>/', api_views.CommentDeleteView.as_view(), name='courses_comments_delete'),
    path('rate-<int:pk>/', api_views.RateCreateView.as_view(), name='courses_vote_rating'),
]