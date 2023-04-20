import pytest
from rest_framework.reverse import reverse

from board.models import Board, BoardMembership
from users.models import User


@pytest.fixture
def board_creation_payload(board_name):
    return {"name": board_name}


def test_cannot_create_board_as_unauthorized_user(api_client, board_creation_payload):
    url = reverse("board:board-list")
    response = api_client.post(url, board_creation_payload)

    assert response.status_code == 401


def test_creates_board(authenticated_client, board_name, board_creation_payload, user):
    url = reverse("board:board-list")
    response = authenticated_client.post(url, board_creation_payload)

    assert response.status_code == 201
    assert Board.objects.filter(owner=user, name=board_name).exists()


def test_creates_board_membership(
    authenticated_client, board_name, board_creation_payload, user
):
    url = reverse("board:board-list")
    response = authenticated_client.post(url, board_creation_payload)

    assert BoardMembership.objects.filter(
        board__slug=response.data["slug"], user=user, role=BoardMembership.Role.ADMIN
    ).exists()


def test_cannot_list_boards_as_unauthorized_user(api_client, board_creation_payload):
    url = reverse("board:board-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_lists_only_member_boards(board, user, authenticated_client):
    other_user = user

    unowned_member_board = Board.objects.create(name="Member board", owner=other_user)
    BoardMembership.objects.create(board=unowned_member_board, user=user)

    other_board = Board.objects.create(name="Other board", owner=other_user)

    should_be_displayed = [board, unowned_member_board]
    excepted_slugs = set([b.slug for b in should_be_displayed])

    url = reverse("board:board-list")
    response = authenticated_client.get(url)
    returned_slugs = set(board["slug"] for board in response.data)

    assert response.status_code == 200
    assert excepted_slugs == returned_slugs


def test_do_not_list_archived_boards(board, authenticated_client):
    board.archived = True
    board.save(update_fields=["archived"])

    url = reverse("board:board-list")
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_board_deletion_archives_board(board, authenticated_client):
    board_id = board.id

    url = reverse("board:board-detail", kwargs={"slug": board.slug})
    response = authenticated_client.delete(url)

    assert response.status_code == 204
    assert not Board.objects.filter(id=board_id).exists()
    board_archived_qs = Board.all_objects.filter(id=board.id)
    assert board_archived_qs
    assert board_archived_qs.get().id == board_id


@pytest.mark.parametrize(
    "role", [BoardMembership.Role.READ_WRITE, BoardMembership.Role.READ_ONLY]
)
def test_board_deletion_requires_admin_membership(authenticated_client, user, role):
    other_user = User.objects.create()
    board = Board.objects.create(name="Non-administrated board", owner=other_user)
    BoardMembership.objects.create(board=board, user=user, role=role)

    url = reverse("board:board-detail", kwargs={"slug": board.slug})
    response = authenticated_client.delete(url)

    assert response.status_code == 403


@pytest.mark.parametrize(
    "role", [BoardMembership.Role.READ_WRITE, BoardMembership.Role.READ_ONLY]
)
def test_board_deletion_of_unrelated_board_returns_404(
    authenticated_client, user, role
):
    other_user = User.objects.create()
    board = Board.objects.create(name="Non-administrated board", owner=other_user)

    url = reverse("board:board-detail", kwargs={"slug": board.slug})
    response = authenticated_client.delete(url)

    assert response.status_code == 404
