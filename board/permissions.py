from rest_framework import permissions

from board.models import BoardMembership


class DetailUnsafeActionsRequiresAdminMembership(permissions.BasePermission):
    message = (
        "Editing board parameters or deleting boards requires admin board's membership"
    )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return BoardMembership.objects.filter(
            board=obj, user=request.user, role=BoardMembership.Role.ADMIN
        ).exists()
