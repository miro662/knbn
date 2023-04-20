from rest_framework.routers import DefaultRouter

from board.views import BoardViewSet

router = DefaultRouter()
router.register("board", BoardViewSet)

urlpatterns = router.urls
