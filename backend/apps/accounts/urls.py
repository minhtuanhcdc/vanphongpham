from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.TaiKhoanViewSet)

urlpatterns = [
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('me/', views.me_view),
    path('', include(router.urls)),
]