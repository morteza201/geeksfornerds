from django.urls import path
from .api_views import GetUsernameView, ChangePasswordView, UserCreateView, UserUpdateProfile, UserDeleteView, UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('get-username/', GetUsernameView.as_view(), name='get_username'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(), name='user_create'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='user_change_password'),
    path('update/<int:pk>/', UserUpdateProfile.as_view(), name='user_update'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<str:username>/', UserView.as_view(), name='user_view'),
]