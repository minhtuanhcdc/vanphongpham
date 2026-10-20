# apps/alerts/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CanhBaoViewSet
from .dashboard_views import thong_ke

router = DefaultRouter()
router.register('canh-bao', CanhBaoViewSet, basename='canh-bao')

urlpatterns = [
    path('dashboard/thong-ke/', thong_ke, name='dashboard-thong-ke'),
] + router.urls