from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from board.models import Board, BoardMembership
from board.serializers import BoardSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        BoardMembership.objects.create(
            board=board, user=self.request.user, role=BoardMembership.Role.ADMIN
        )
