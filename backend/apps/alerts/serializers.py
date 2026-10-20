# apps/alerts/serializers.py
from rest_framework import serializers
from .models import CanhBao


class CanhBaoSerializer(serializers.ModelSerializer):
    ten_sp = serializers.CharField(source='san_pham.ten_sp', read_only=True)

    class Meta:
        model = CanhBao
        fields = [
            'ma_cb', 'san_pham', 'ten_sp', 'loai_canh_bao',
            'so_luong_ton', 'noi_dung', 'ngay_canh_bao', 'da_xu_ly',
        ]
        read_only_fields = ['ma_cb', 'ngay_canh_bao']