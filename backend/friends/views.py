from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from friends.models import FriendRequest
from friends.serializers import FriendRequestSerializer
from notifications.utils import envoyer_notification

User = get_user_model()


class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = User.objects.get(id=serializer.validated_data['to_user_id'])
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user,
            defaults={'status': 'pending'},
        )
        if created:
            envoyer_notification(
                to_user,
                'friend_request',
                f"{request.user.display_name} vous a envoyé une demande d'ami.",
            )
        output = FriendRequestSerializer(friend_request, context={'request': request})
        return Response(output.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.status = 'accepted'
        friend_request.save(update_fields=['status'])
        return Response({'detail': 'Demande acceptée.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.status = 'rejected'
        friend_request.save(update_fields=['status'])
        return Response({'detail': 'Demande refusée.'}, status=status.HTTP_200_OK)


class FriendListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        accepted_requests = FriendRequest.objects.filter(
            Q(from_user=request.user) | Q(to_user=request.user),
            status='accepted',
        )
        friend_ids = [
            fr.to_user_id if fr.from_user_id == request.user.id else fr.from_user_id
            for fr in accepted_requests
        ]
        friends = User.objects.filter(id__in=friend_ids)
        data = [
            {
                'id': friend.id,
                'display_name': friend.display_name,
                'email': friend.email,
                'avatar': friend.avatar.url if friend.avatar else None,
            }
            for friend in friends
        ]
        return Response(data)
