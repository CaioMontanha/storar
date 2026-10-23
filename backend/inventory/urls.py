from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import ProductViewSet, StoreViewSet, dashboard

router = DefaultRouter()
router.register("stores", StoreViewSet, basename="store")
router.register("products", ProductViewSet, basename="product")
urlpatterns = [path("dashboard/", dashboard, name="dashboard"), path("", include(router.urls))]
