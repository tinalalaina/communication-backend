from django.urls import path

from users.views import LoginView, LogoutView, MeView, PublicProfileView, RefreshView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('<int:pk>/', PublicProfileView.as_view(), name='public-profile'),
]
