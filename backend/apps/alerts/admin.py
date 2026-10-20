from django.contrib import admin
from .models import CanhBao

@admin.register(CanhBao)
class CanhBaoAdmin(admin.ModelAdmin):
    list_display = ('ma_cb', 'san_pham', 'loai_canh_bao',
                    'so_luong_ton', 'da_xu_ly', 'ngay_canh_bao')
    list_filter = ('loai_canh_bao', 'da_xu_ly')