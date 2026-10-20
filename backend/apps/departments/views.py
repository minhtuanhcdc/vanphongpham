from rest_framework import viewsets
from .models import KhoaPhong
from .serializers import KhoaPhongSerializer


class KhoaPhongViewSet(viewsets.ModelViewSet):
    queryset = KhoaPhong.objects.all()
    serializer_class = KhoaPhongSerializer
    search_fields = ['ten_kp']
