from django.urls import path, include
from rest_framework import routers
from blogging.views import (
    PostListView,
    PostDetailView,
    add_model,
    UserViewSet,
    PostViewSet,
    CategoryViewSet,
    LatestPostsFeed,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"posts", PostViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", PostListView.as_view(), name="blog_index"),
    path("add/", add_model, name="add_post"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
]
