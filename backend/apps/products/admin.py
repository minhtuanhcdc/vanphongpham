# apps/products/admin.py
from django.contrib import admin
from .models import DanhMuc, NhaCungCap, SanPham


@admin.register(DanhMuc)
class DanhMucAdmin(admin.ModelAdmin):
    list_display = ['ma_dm', 'ten_dm', 'mo_ta']
    search_fields = ['ten_dm']


@admin.register(NhaCungCap)
class NhaCungCapAdmin(admin.ModelAdmin):
    list_display = ['ma_ncc', 'ten_ncc', 'dien_thoai', 'email', 'trang_thai']
    search_fields = ['ten_ncc', 'dien_thoai']
    list_filter = ['trang_thai']


@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = [
        'ma_sp', 'ten_sp', 'danh_muc', 'don_vi_tinh',
        'muc_ton_toi_thieu', 'muc_ton_toi_da', 'trang_thai',
    ]
    list_filter = ['trang_thai', 'danh_muc']
    search_fields = ['ten_sp']