from django.contrib import admin

from board.models import Board, BoardMembership


class BoardMembershipAdmin(admin.StackedInline):
    model = BoardMembership
    extra = 0


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    inlines = [BoardMembershipAdmin]
    fields = ["name", "slug", "owner", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
