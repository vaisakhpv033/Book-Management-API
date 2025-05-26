from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ReadingListViewSet, AuthorViewSet, GenreViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("reading-list", ReadingListViewSet, basename="reading-list")
router.register("authors", AuthorViewSet, basename="authors")
router.register("genres", GenreViewSet, basename="genres")


urlpatterns = router.urls
