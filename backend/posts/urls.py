from django.urls import include, path
from rest_framework.routers import SimpleRouter

from posts.views import CommentViewSet, PostViewSet

router = SimpleRouter()
router.register('', PostViewSet, basename='post')

comment_list = CommentViewSet.as_view({'get': 'list', 'post': 'create'})
comment_detail = CommentViewSet.as_view({'delete': 'destroy'})

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:post_id>/comments/', comment_list, name='comment-list'),
    path('<uuid:post_id>/comments/<uuid:pk>/', comment_detail, name='comment-detail'),
]
