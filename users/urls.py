from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView
from django.urls import path

urlpatterns = [
    # users
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
