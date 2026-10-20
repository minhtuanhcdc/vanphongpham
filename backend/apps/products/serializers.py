# apps/products/serializers.py
from rest_framework import serializers
from django.db.models import Sum
from .models import DanhMuc, NhaCungCap, SanPham


class DanhMucSerializer(serializers.ModelSerializer):
    so_san_pham = serializers.SerializerMethodField()

    class Meta:
        model = DanhMuc
        fields = ['ma_dm', 'ten_dm', 'mo_ta', 'so_san_pham']

    def get_so_san_pham(self, obj):
        return obj.san_phams.count()


class NhaCungCapSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhaCungCap
        fields = '__all__'


class SanPhamSerializer(serializers.ModelSerializer):
    ten_dm = serializers.CharField(source='danh_muc.ten_dm', read_only=True)
    so_luong_ton = serializers.SerializerMethodField()
    trang_thai_ton = serializers.SerializerMethodField()
    tong_nhap = serializers.SerializerMethodField()   # ➕
    tong_xuat = serializers.SerializerMethodField()   # ➕

    class Meta:
        model = SanPham
        fields = [
            'ma_sp', 'ten_sp', 'danh_muc', 'ten_dm',
            'don_vi_tinh', 'muc_ton_toi_thieu', 'muc_ton_toi_da',
            'han_su_dung', 'hinh_anh', 'trang_thai',
            'so_luong_ton', 'trang_thai_ton',
            'tong_nhap', 'tong_xuat',
        ]

    def get_so_luong_ton(self, obj):
        # Ưu tiên ton_map từ context
        ton_map = self.context.get('ton_map')
        if ton_map is not None:
            return ton_map.get(obj.ma_sp, 0)

        from apps.inventory.models import ChiTietPhieuNhap
        kq = ChiTietPhieuNhap.objects.filter(
            san_pham_id=obj.ma_sp,
            phieu_nhap__trang_thai='NHAP',
        ).aggregate(tong=Sum('so_luong_con_lai'))
        return kq['tong'] or 0

    def get_trang_thai_ton(self, obj):
        ton = self.get_so_luong_ton(obj)
        if ton == 0:
            return 'HET_HANG'
        if ton <= obj.muc_ton_toi_thieu:
            return 'SAP_HET'
        if ton > obj.muc_ton_toi_da:
            return 'TON_CAO'
        return 'BINH_THUONG'

    def get_tong_nhap(self, obj):
        nhap_map = self.context.get('nhap_map')
        if nhap_map is not None:
            return nhap_map.get(obj.ma_sp, 0)

        from apps.inventory.models import ChiTietPhieuNhap
        kq = ChiTietPhieuNhap.objects.filter(
            san_pham_id=obj.ma_sp,
            phieu_nhap__trang_thai='NHAP',
        ).aggregate(tong=Sum('so_luong'))
        return kq['tong'] or 0

    def get_tong_xuat(self, obj):
        xuat_map = self.context.get('xuat_map')
        if xuat_map is not None:
            return xuat_map.get(obj.ma_sp, 0)

        from apps.inventory.models import ChiTietPhieuXuat
        kq = ChiTietPhieuXuat.objects.filter(
            san_pham_id=obj.ma_sp,
            phieu_xuat__trang_thai='XUAT',
        ).aggregate(tong=Sum('so_luong'))
        return kq['tong'] or 0