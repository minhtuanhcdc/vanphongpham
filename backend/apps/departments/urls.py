# apps/departments/urls.py
from rest_framework.routers import DefaultRouter
from .views import KhoaPhongViewSet

router = DefaultRouter()
router.register('khoa-phong', KhoaPhongViewSet, basename='khoa-phong')

urlpatterns = router.urls