from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserLoginView, UserRegistrationView, UserProfileView

app_name = 'users'

urlpatterns = [
    path('login/', cache_page(60)(UserLoginView.as_view()), name='login'),
    path('registration/', cache_page(60)(UserRegistrationView.as_view()), name='registration'),
    path('profile/<int:pk>/', login_required(cache_page(60)(UserProfileView.as_view())), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
