from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from posts.models import Post, PostRate
from posts.services import score_service
from users.models import UserProfile


class PostRateSerializer(serializers.ModelSerializer):
    score = serializers.ChoiceField(choices=PostRate.Score.choices)
    rater_uuid = serializers.UUIDField()
    post_uuid = serializers.UUIDField()
    class Meta:
        model = PostRate
        fields = ("post_uuid", "rater_uuid", "score")

    def create(self, validated_data):
        post = get_object_or_404(Post.objects.all(), uuid=validated_data['post_uuid'])
        rater = get_object_or_404(UserProfile.objects.all(), uuid=validated_data['rater_uuid'])
        if previous := PostRate.objects.filter(
            post_uuid=validated_data['post_uuid'],
            rater_uuid=validated_data['rater_uuid'],
            expired_at__isnull=True,
        ).first():
            previous.expired_at = timezone.now()
            previous.save()
        rate = PostRate(
            post_uuid=validated_data['post_uuid'],
            rater_uuid=validated_data['rater_uuid'],
            score=validated_data['score'],
        )
        rate.save()
        score = post.score
        score_service.update_score(post, score if score else 0)
        return rate

