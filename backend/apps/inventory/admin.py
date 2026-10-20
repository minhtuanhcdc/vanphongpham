# apps/inventory/admin.py
from django.contrib import admin
from .models import (
    PhieuNhap, ChiTietPhieuNhap,
    PhieuXuat, ChiTietPhieuXuat,
    LichSuKho,
)


class ChiTietPhieuNhapInline(admin.TabularInline):
    model = ChiTietPhieuNhap
    extra = 0
    readonly_fields = ['so_luong_con_lai']


@admin.register(PhieuNhap)
class PhieuNhapAdmin(admin.ModelAdmin):
    list_display = ['ma_pn', 'so_phieu', 'nha_cung_cap',
                    'ngay_nhap', 'trang_thai']
    list_filter = ['trang_thai', 'ngay_nhap']
    search_fields = ['so_phieu', 'so_hoa_don']
    inlines = [ChiTietPhieuNhapInline]


class ChiTietPhieuXuatInline(admin.TabularInline):
    model = ChiTietPhieuXuat
    extra = 0


@admin.register(PhieuXuat)
class PhieuXuatAdmin(admin.ModelAdmin):
    list_display = ['ma_px', 'so_phieu', 'khoa_phong',
                    'ngay_xuat', 'trang_thai']
    list_filter = ['trang_thai', 'ngay_xuat', 'khoa_phong']
    search_fields = ['so_phieu', 'nguoi_nhan']
    inlines = [ChiTietPhieuXuatInline]


@admin.register(LichSuKho)
class LichSuKhoAdmin(admin.ModelAdmin):
    list_display = ['ma_lsk', 'san_pham', 'loai',
                    'so_luong_thay_doi', 'so_luong_sau',
                    'tham_chieu', 'thoi_gian']
    list_filter = ['loai', 'thoi_gian']
    search_fields = ['san_pham__ten_sp', 'tham_chieu']
    readonly_fields = ['so_luong_sau', 'thoi_gian']