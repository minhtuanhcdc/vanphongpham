# apps/inventory/models.py
from django.db import models, transaction
from django.db.models import Sum
from django.core.exceptions import ValidationError


# ==================== PHIẾU NHẬP ====================

class PhieuNhap(models.Model):
    TRANG_THAI = (('NHAP', 'Đã nhập'), ('HUY', 'Đã hủy'))

    ma_pn = models.AutoField(primary_key=True)
    so_phieu = models.CharField(max_length=50, unique=True)
    ngay_nhap = models.DateTimeField(auto_now_add=True)
    nha_cung_cap = models.ForeignKey(
        'products.NhaCungCap',
        on_delete=models.PROTECT,
        null=True, blank=True, db_column='ma_ncc',
        related_name='phieu_nhaps',
    )
    so_hoa_don = models.CharField(max_length=50, blank=True, null=True)
    nguoi_lap = models.ForeignKey(
        'accounts.TaiKhoan',
        on_delete=models.SET_NULL,
        null=True, blank=True, db_column='ma_tk',
        related_name='phieu_nhap_lap',
    )
    ghi_chu = models.CharField(max_length=255, blank=True, null=True)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI, default='NHAP')

    class Meta:
        db_table = 'phieu_nhap'
        ordering = ['-ngay_nhap']

    def __str__(self):
        return f'PN-{self.ma_pn}'

    # ---------- NGHIỆP VỤ ----------
    @classmethod
    @transaction.atomic
    def tao_phieu(cls, *, so_phieu, nguoi_lap_id, chi_tiet: list,
                  nha_cung_cap_id=None, so_hoa_don=None, ghi_chu=None):
        """
        chi_tiet: [{'san_pham_id': int, 'so_luong': int,
                    'don_gia_nhap': Decimal|None, 'han_su_dung': date|None}]
        """
        if not chi_tiet:
            raise ValidationError('Chưa có chi tiết phiếu nhập.')

        pn = cls.objects.create(
            so_phieu=so_phieu,
            nha_cung_cap_id=nha_cung_cap_id,
            nguoi_lap_id=nguoi_lap_id,
            so_hoa_don=so_hoa_don,
            ghi_chu=ghi_chu,
        )
        for row in chi_tiet:
            so_luong = int(row['so_luong'])
            if so_luong <= 0:
                raise ValidationError(
                    f'Số lượng nhập phải > 0 (sản phẩm id={row["san_pham_id"]}).'
                )
            ChiTietPhieuNhap.objects.create(
                phieu_nhap=pn,
                san_pham_id=row['san_pham_id'],
                so_luong=so_luong,
                don_gia_nhap=row.get('don_gia_nhap'),
                han_su_dung=row.get('han_su_dung'),
                so_luong_con_lai=so_luong,   # khởi tạo = số lượng nhập
            )
            ton_truoc = LichSuKho.ton_kho(row['san_pham_id'])
            LichSuKho.objects.create(
                san_pham_id=row['san_pham_id'],
                loai='NHAP',
                so_luong_thay_doi=so_luong,
                so_luong_sau=ton_truoc + so_luong,
                tham_chieu=pn.so_phieu,
                nguoi_thuc_hien_id=nguoi_lap_id,
            )
        return pn


# ==================== CHI TIẾT NHẬP ====================

class ChiTietPhieuNhap(models.Model):
    phieu_nhap = models.ForeignKey(
        PhieuNhap, related_name='chi_tiet',
        on_delete=models.CASCADE, db_column='ma_pn',
    )
    san_pham = models.ForeignKey(
        'products.SanPham',
        on_delete=models.PROTECT,
        db_column='ma_sp', related_name='chi_tiet_nhap',
    )
    so_luong = models.IntegerField()
    don_gia_nhap = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    han_su_dung = models.DateField(null=True, blank=True)
    so_luong_con_lai = models.IntegerField(default=0)

    class Meta:
        db_table = 'chi_tiet_phieu_nhap'
        constraints = [
            models.CheckConstraint(
                check=models.Q(so_luong__gt=0),
                name='ctpn_so_luong_duong',
            ),
            models.CheckConstraint(
                check=models.Q(so_luong_con_lai__gte=0),
                name='ctpn_con_lai_khong_am',
            ),
            models.CheckConstraint(
                check=models.Q(so_luong_con_lai__lte=models.F('so_luong')),
                name='ctpn_con_lai_khong_vuot_so_luong',
            ),
        ]


# ==================== PHIẾU XUẤT ====================

class PhieuXuat(models.Model):
    TRANG_THAI = (('XUAT', 'Đã xuất'), ('HUY', 'Đã hủy'))

    ma_px = models.AutoField(primary_key=True)
    so_phieu = models.CharField(max_length=50, unique=True)
    ngay_xuat = models.DateTimeField(auto_now_add=True)
    khoa_phong = models.ForeignKey(
        'departments.KhoaPhong',
        on_delete=models.PROTECT,
        db_column='ma_kp', related_name='phieu_xuats',
    )
    nguoi_lap = models.ForeignKey(
        'accounts.TaiKhoan',
        on_delete=models.SET_NULL,
        null=True, blank=True, db_column='ma_tk',
        related_name='phieu_xuat_lap',
    )
    nguoi_nhan = models.CharField(max_length=100, blank=True, null=True)
    ly_do = models.CharField(max_length=255, blank=True, null=True)
    ghi_chu = models.CharField(max_length=255, blank=True, null=True)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI, default='XUAT')

    class Meta:
        db_table = 'phieu_xuat'
        ordering = ['-ngay_xuat']

    def __str__(self):
        return f'PX-{self.ma_px}'

    # ---------- NGHIỆP VỤ ----------
    @classmethod
    @transaction.atomic
    def tao_phieu(cls, *, so_phieu, khoa_phong_id, nguoi_lap_id,
                  chi_tiet: list, nguoi_nhan=None, ly_do=None, ghi_chu=None):
        """
        chi_tiet: [{'san_pham_id': int, 'so_luong': int}]
        - Kiểm tra tồn trước khi xuất (tổng theo sản phẩm).
        - Trừ FIFO vào các lô ChiTietPhieuNhap còn so_luong_con_lai > 0.
        """
        if not chi_tiet:
            raise ValidationError('Chưa có chi tiết phiếu xuất.')

        # 1. Gom số lượng theo sản phẩm
        tong_theo_sp = {}
        for row in chi_tiet:
            sl = int(row['so_luong'])
            if sl <= 0:
                raise ValidationError(
                    f'Số lượng xuất phải > 0 (sản phẩm id={row["san_pham_id"]}).'
                )
            tong_theo_sp[row['san_pham_id']] = (
                tong_theo_sp.get(row['san_pham_id'], 0) + sl
            )

        # 2. Kiểm tra tồn
        for sp_id, sl_can in tong_theo_sp.items():
            con = LichSuKho.ton_kho(sp_id)
            if con < sl_can:
                raise ValidationError(
                    f'Sản phẩm id={sp_id} không đủ tồn '
                    f'(cần {sl_can}, còn {con}).'
                )

        # 3. Tạo phiếu
        px = cls.objects.create(
            so_phieu=so_phieu,
            khoa_phong_id=khoa_phong_id,
            nguoi_lap_id=nguoi_lap_id,
            nguoi_nhan=nguoi_nhan,
            ly_do=ly_do,
            ghi_chu=ghi_chu,
        )

        # 4. Tạo chi tiết + trừ FIFO vào lô + ghi LichSuKho
        for row in chi_tiet:
            sp_id = row['san_pham_id']
            sl_xuat = int(row['so_luong'])

            ChiTietPhieuXuat.objects.create(
                phieu_xuat=px,
                san_pham_id=sp_id,
                so_luong=sl_xuat,
            )

            # FIFO: lô cũ nhất (theo ngày nhập) còn hàng trước
            con_can_tru = sl_xuat
            lo_hang = (
                ChiTietPhieuNhap.objects
                .filter(san_pham_id=sp_id, so_luong_con_lai__gt=0)
                .order_by('phieu_nhap__ngay_nhap', 'phieu_nhap_id')
            )
            for lo in lo_hang:
                if con_can_tru <= 0:
                    break
                tru = min(lo.so_luong_con_lai, con_can_tru)
                lo.so_luong_con_lai -= tru
                lo.save(update_fields=['so_luong_con_lai'])
                con_can_tru -= tru

            # Ghi lịch sử kho
            ton_truoc = LichSuKho.ton_kho(sp_id) + sl_xuat  # vì đã trừ sau
            # Lưu ý: ton_kho() đọc từ LichSuKho — chưa ghi dòng mới, nên
            # ton_truoc = tồn hiện tại (đã bao gồm các lần xuất trước trong cùng phiếu)
            ton_hien_tai = LichSuKho.ton_kho(sp_id)
            LichSuKho.objects.create(
                san_pham_id=sp_id,
                loai='XUAT',
                so_luong_thay_doi=-sl_xuat,
                so_luong_sau=ton_hien_tai - sl_xuat,
                tham_chieu=px.so_phieu,
                nguoi_thuc_hien_id=nguoi_lap_id,
            )

        return px


# ==================== CHI TIẾT XUẤT ====================

class ChiTietPhieuXuat(models.Model):
    phieu_xuat = models.ForeignKey(
        PhieuXuat, related_name='chi_tiet',
        on_delete=models.CASCADE, db_column='ma_px',
    )
    san_pham = models.ForeignKey(
        'products.SanPham',
        on_delete=models.PROTECT,
        db_column='ma_sp', related_name='chi_tiet_xuat',
    )
    so_luong = models.IntegerField()

    class Meta:
        db_table = 'chi_tiet_phieu_xuat'
        constraints = [
            models.CheckConstraint(
                check=models.Q(so_luong__gt=0),
                name='ctpx_so_luong_duong',
            ),
        ]


# ==================== LỊCH SỬ KHO ====================

class LichSuKho(models.Model):
    LOAI = (
        ('NHAP', 'Nhập kho'),
        ('XUAT', 'Xuất kho'),
        ('DIEU_CHINH', 'Điều chỉnh'),
        ('KIEM_KE', 'Kiểm kê'),
    )
    ma_lsk = models.AutoField(primary_key=True)
    san_pham = models.ForeignKey(
        'products.SanPham', on_delete=models.PROTECT,
        db_column='ma_sp', related_name='lich_su_kho',
    )
    loai = models.CharField(max_length=20, choices=LOAI)
    so_luong_thay_doi = models.IntegerField()
    so_luong_sau = models.IntegerField()
    tham_chieu = models.CharField(max_length=50, blank=True, null=True)
    thoi_gian = models.DateTimeField(auto_now_add=True)
    nguoi_thuc_hien = models.ForeignKey(
        'accounts.TaiKhoan', on_delete=models.SET_NULL,
        null=True, blank=True, db_column='ma_tk',
    )
    ghi_chu = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'lich_su_kho'
        ordering = ['-thoi_gian']
        indexes = [
            models.Index(fields=['san_pham', '-thoi_gian']),
        ]

    # ---------- HELPER ----------
    @staticmethod
    def ton_kho(ma_sp: int) -> int:
        return LichSuKho.objects.filter(san_pham_id=ma_sp).aggregate(
            t=Sum('so_luong_thay_doi')
        )['t'] or 0

    @staticmethod
    def ton_kho_tat_ca() -> dict:
        rows = (
            LichSuKho.objects
            .values('san_pham_id')
            .annotate(t=Sum('so_luong_thay_doi'))
        )
        return {r['san_pham_id']: (r['t'] or 0) for r in rows}