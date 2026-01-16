from rest_framework import serializers

from friends.models import FriendRequest
from users.serializers import UserPublicSerializer


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserPublicSerializer(read_only=True)
    to_user = UserPublicSerializer(read_only=True)
    to_user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'to_user_id', 'status', 'created_at']
        read_only_fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
