from django.urls import path
from .views import getTokensForUser, refreshAccessToken

urlpatterns = [
    path('token/', getTokensForUser, name='token_obtain_pair_url'),
    path('token/refresh/', refreshAccessToken, name='token_refresh_url'),
]