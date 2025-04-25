from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_subscription"
            )
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.following}"
