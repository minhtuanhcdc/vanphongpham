#app/departments/serializers.py
from rest_framework import serializers
from .models import KhoaPhong


class KhoaPhongSerializer(serializers.ModelSerializer):
    so_phieu_xuat = serializers.SerializerMethodField()

    class Meta:
        model = KhoaPhong
        fields = ['ma_kp', 'ten_kp', 'mo_ta', 'trang_thai', 'so_phieu_xuat']

    def get_so_phieu_xuat(self, obj):
        try:
            return obj.phieu_xuats.count()
        except Exception:
            return 0
