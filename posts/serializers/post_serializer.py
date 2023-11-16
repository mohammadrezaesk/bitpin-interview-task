from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from posts.models import Post
from posts.services import score_service
from users.models import UserProfile
from users.serializers.user_profile_serializer import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer("author", read_only=True)
    score = serializers.SerializerMethodField()
    author_uuid = serializers.UUIDField(write_only=True)

    def get_score(self, obj: Post) -> float:
        return score_service.get_score(obj)

    class Meta:
        model = Post
        read_only_fields = ("author", "created_at", "score", "uuid")
        fields = ("author", "content", "created_at", "score", "uuid", "author_uuid")
        write_only_fields = ("content", "author_uuid")

    def create(self, validated_data):
        author = get_object_or_404(UserProfile.objects.all(), uuid=validated_data['author_uuid'])
        post = Post(
            content=validated_data['content'],
            author=author
        )
        post.save()
        return post

