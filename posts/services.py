from posts.models import Post
from redis_repository import redis_repository


class ScoreService:

    @staticmethod
    def _get_score_redis_key(post_id):
        return f"post_score_{post_id}"

    def update_score(self, post: Post, score: float):
        redis_repository.store(self._get_score_redis_key(post.id), score)

    def get_score(self, post: Post) -> float:
        if score := redis_repository.get(self._get_score_redis_key(post.id)):
            return float(score)
        score = post.score
        self.update_score(post, score if score else 0)
        return score if score else 0


score_service = ScoreService()

