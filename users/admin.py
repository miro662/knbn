from django.contrib import admin

from board.admin import BoardMembershipAdmin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [BoardMembershipAdmin]
    pass
