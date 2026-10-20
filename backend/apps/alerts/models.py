# apps/alert/models.py
from django.db import models
from apps.products.models import SanPham


class CanhBao(models.Model):
    LOAI = [
        ('SAP_HET', 'Sắp hết'),
        ('HET_HANG', 'Hết hàng'),
        ('TON_CAO', 'Tồn cao'),
    ]
    ma_cb = models.AutoField(primary_key=True)
    san_pham = models.ForeignKey(
        SanPham, on_delete=models.CASCADE,
        db_column='ma_sp', related_name='canh_baos',
    )
    loai_canh_bao = models.CharField(max_length=20, choices=LOAI)
    so_luong_ton = models.IntegerField()          # snapshot tại thời điểm tạo
    noi_dung = models.CharField(max_length=255)
    ngay_canh_bao = models.DateTimeField(auto_now_add=True)
    da_xu_ly = models.BooleanField(default=False)

    class Meta:
        db_table = 'canh_bao'
        ordering = ['-ngay_canh_bao']
        indexes = [
            models.Index(fields=['san_pham', 'da_xu_ly']),
        ]