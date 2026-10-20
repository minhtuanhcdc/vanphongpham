# apps/inventory/urls.py
from rest_framework.routers import DefaultRouter
from .views import PhieuNhapViewSet, PhieuXuatViewSet, LichSuKhoViewSet

router = DefaultRouter()
router.register('phieu-nhap', PhieuNhapViewSet, basename='phieu-nhap')
router.register('phieu-xuat', PhieuXuatViewSet, basename='phieu-xuat')
router.register('lich-su-kho', LichSuKhoViewSet, basename='lich-su-kho')

urlpatterns = router.urls