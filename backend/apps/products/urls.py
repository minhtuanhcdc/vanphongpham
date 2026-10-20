# apps/products/urls.py
from rest_framework.routers import DefaultRouter
from .views import DanhMucViewSet, NhaCungCapViewSet, SanPhamViewSet

router = DefaultRouter()
router.register('danh-muc', DanhMucViewSet, basename='danh-muc')
router.register('nha-cung-cap', NhaCungCapViewSet, basename='nha-cung-cap')
router.register('san-pham', SanPhamViewSet, basename='san-pham')

urlpatterns = router.urls