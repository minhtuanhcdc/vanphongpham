from django.db import models


class DanhMuc(models.Model):
    ma_dm = models.AutoField(primary_key=True)
    ten_dm = models.CharField(max_length=100)
    mo_ta = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'danh_muc'
        ordering = ['ten_dm']

    def __str__(self):
        return self.ten_dm


class NhaCungCap(models.Model):
    ma_ncc = models.AutoField(primary_key=True)
    ten_ncc = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=200, blank=True, null=True)
    dien_thoai = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    trang_thai = models.BooleanField(default=True)

    class Meta:
        db_table = 'nha_cung_cap'
        ordering = ['ten_ncc']

    def __str__(self):
        return self.ten_ncc


class SanPham(models.Model):
    ma_sp = models.AutoField(primary_key=True)
    ten_sp = models.CharField(max_length=100)
    danh_muc = models.ForeignKey(
        DanhMuc, on_delete=models.SET_NULL,
        null=True, blank=True, db_column='ma_dm',
        related_name='san_phams',
    )
    don_vi_tinh = models.CharField(max_length=20, blank=True, null=True)
    muc_ton_toi_thieu = models.IntegerField(default=5)
    muc_ton_toi_da = models.IntegerField(default=1000)
    han_su_dung = models.DateField(null=True, blank=True)
    hinh_anh = models.ImageField(upload_to='sanpham/', blank=True, null=True)
    trang_thai = models.BooleanField(default=True)

    class Meta:
        db_table = 'san_pham'
        ordering = ['ten_sp']
        constraints = [
            models.CheckConstraint(
                check=models.Q(muc_ton_toi_thieu__gte=0),
                name='sp_muc_ton_toi_thieu_khong_am',
            ),
            models.CheckConstraint(
                check=models.Q(muc_ton_toi_da__gte=models.F('muc_ton_toi_thieu')),
                name='sp_muc_ton_toi_da_lon_hon_toi_thieu',
            ),
        ]

    def __str__(self):
        return self.ten_sp