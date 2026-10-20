from django.db import models


class KhoaPhong(models.Model):
    ma_kp = models.AutoField(primary_key=True)
    ten_kp = models.CharField(max_length=100)
    mo_ta = models.CharField(max_length=255, blank=True, null=True)
    trang_thai = models.BooleanField(default=True)

    class Meta:
        db_table = 'khoa_phong'
        ordering = ['ten_kp']

    def __str__(self):
        return self.ten_kp
