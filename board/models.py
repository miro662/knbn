from django.db import models
from django.utils.text import slugify

from users.models import User


class BoardQuerySet(models.QuerySet):
    def available_to(self, user):
        return self.filter(members=user)


class BoardManager(models.Manager):
    def get_queryset(self):
        return BoardQuerySet(self.model, using=self._db).filter(archived=False)

    def available_to(self, user):
        return self.get_queryset().available_to(user)


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
    archived = models.BooleanField(default=False)

    objects = BoardManager()
    all_objects = BoardQuerySet.as_manager()

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
