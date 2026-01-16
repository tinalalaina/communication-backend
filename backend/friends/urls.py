from django.urls import include, path
from rest_framework.routers import SimpleRouter

from friends.views import FriendListViewSet, FriendRequestViewSet

router = SimpleRouter()
router.register('requests', FriendRequestViewSet, basename='friend-requests')
router.register('list', FriendListViewSet, basename='friend-list')

urlpatterns = [
    path('', include(router.urls)),
]
