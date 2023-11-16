import uuid
from django.db import models
from django.db.models import Avg

from users import models as users_models


class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    author = models.ForeignKey(users_models.UserProfile, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(null=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def score(self) -> float:
        return PostRate.objects.filter(post_uuid=self.uuid, expired_at__isnull=True).aggregate(
            average_rating=Avg("score")
        ).get('average_rating', 0)


class PostRate(models.Model):
    class Score(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    rater_uuid = models.UUIDField(null=False)
    post_uuid = models.UUIDField(null=False)
    score = models.IntegerField(choices=Score.choices)
    rated_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        indexes = [
            models.Index(fields=["post_uuid"]),
            models.Index(fields=["post_uuid", "rater_uuid"], name="post_rater_idx"),
        ]
        unique_together = ("rater_uuid", "post_uuid", "expired_at")
