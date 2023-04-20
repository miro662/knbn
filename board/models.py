from django.db import models
from django.utils.text import slugify

from users.models import User


class Board(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(
        User, related_name="owned_boards", on_delete=models.PROTECT
    )
    members = models.ManyToManyField(
        User, through="BoardMembership", related_name="boards"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.get_full_name()}'s {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.owner.username + "-" + self.name)
        return super().save(*args, **kwargs)


class BoardMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "A", "Administrator"
        READ_WRITE = "W", "Read and write access"
        READ_ONLY = "R", "Read-only access"

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=1, choices=Role.choices, default=Role.READ_WRITE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "user"], name="one_membership_per_user_per_board"
            )
        ]
