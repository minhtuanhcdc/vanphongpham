# apps/inventory/serializers.py
from rest_framework import serializers
from .models import (
    PhieuNhap, ChiTietPhieuNhap,
    PhieuXuat, ChiTietPhieuXuat,
    LichSuKho,
)


# ==================== NHẬP ====================

class ChiTietPhieuNhapSerializer(serializers.ModelSerializer):
    ten_sp = serializers.CharField(source='san_pham.ten_sp', read_only=True)

    class Meta:
        model = ChiTietPhieuNhap
        fields = ['id', 'san_pham', 'ten_sp', 'so_luong',
                  'don_gia_nhap', 'han_su_dung']


class PhieuNhapSerializer(serializers.ModelSerializer):
    chi_tiet = ChiTietPhieuNhapSerializer(many=True)
    ten_ncc = serializers.CharField(source='nha_cung_cap.ten_ncc', read_only=True)
    ten_nguoi_lap = serializers.CharField(source='nguoi_lap.ho_ten', read_only=True)

    class Meta:
        model = PhieuNhap
        fields = [
            'ma_pn', 'so_phieu', 'ngay_nhap',
            'nha_cung_cap', 'ten_ncc', 'so_hoa_don',
            'nguoi_lap', 'ten_nguoi_lap',
            'ghi_chu', 'trang_thai',
            'chi_tiet',
        ]
        read_only_fields = ['ma_pn', 'ngay_nhap', 'nguoi_lap']

    def validate_chi_tiet(self, value):
        if not value:
            raise serializers.ValidationError('Chưa có chi tiết phiếu nhập')
        return value

    def validate_so_phieu(self, value):
        # ✅ báo lỗi 400 thay vì 500 khi trùng số phiếu
        qs = PhieuNhap.objects.filter(so_phieu=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Số phiếu đã tồn tại')
        return value


# ==================== XUẤT ====================

class ChiTietPhieuXuatSerializer(serializers.ModelSerializer):
    ten_sp = serializers.CharField(source='san_pham.ten_sp', read_only=True)

    class Meta:
        model = ChiTietPhieuXuat
        fields = ['id', 'san_pham', 'ten_sp', 'so_luong']


class PhieuXuatSerializer(serializers.ModelSerializer):
    chi_tiet = ChiTietPhieuXuatSerializer(many=True)
    ten_kp = serializers.CharField(source='khoa_phong.ten_kp', read_only=True)
    ten_nguoi_lap = serializers.CharField(source='nguoi_lap.ho_ten', read_only=True)

    class Meta:
        model = PhieuXuat
        fields = [
            'ma_px', 'so_phieu', 'ngay_xuat',
            'khoa_phong', 'ten_kp',
            'nguoi_lap', 'ten_nguoi_lap',
            'nguoi_nhan', 'ly_do', 'ghi_chu', 'trang_thai',
            'chi_tiet',
        ]
        read_only_fields = ['ma_px', 'ngay_xuat', 'nguoi_lap']

    def validate_chi_tiet(self, value):
        if not value:
            raise serializers.ValidationError('Chưa có chi tiết phiếu xuất')
        return value

    def validate_so_phieu(self, value):
        qs = PhieuXuat.objects.filter(so_phieu=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Số phiếu đã tồn tại')
        return value


# ==================== TỒN KHO ====================

class LichSuKhoSerializer(serializers.ModelSerializer):
    ten_sp = serializers.CharField(source='san_pham.ten_sp', read_only=True)
    ten_nguoi_thuc_hien = serializers.CharField(
        source='nguoi_thuc_hien.ho_ten', read_only=True
    )

    class Meta:
        model = LichSuKho
        fields = [
            'ma_lsk', 'san_pham', 'ten_sp', 'loai',
            'so_luong_thay_doi', 'so_luong_sau',
            'tham_chieu', 'thoi_gian',
            'nguoi_thuc_hien', 'ten_nguoi_thuc_hien', 'ghi_chu',
        ]
        read_only_fields = ['ma_lsk', 'thoi_gian']