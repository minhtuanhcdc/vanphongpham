# apps/alerts/dashboard_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.expressions import RawSQL

from apps.products.models import SanPham
from apps.inventory.models import (
    PhieuNhap, PhieuXuat, ChiTietPhieuNhap,
)
from apps.alerts.models import CanhBao


@api_view(['GET'])
def thong_ke(request):
    so_san_pham = SanPham.objects.filter(trang_thai=True).count()
    so_phieu_nhap = PhieuNhap.objects.filter(trang_thai='NHAP').count()
    so_phieu_xuat = PhieuXuat.objects.filter(trang_thai='XUAT').count()
    so_canh_bao = CanhBao.objects.filter(da_xu_ly=False).count()

    # Tổng giá trị tồn = SUM(so_luong_con_lai * don_gia_nhap)
    gia_tri_qs = ChiTietPhieuNhap.objects.filter(
        phieu_nhap__trang_thai='NHAP',
        don_gia_nhap__isnull=False,
    ).aggregate(
        tong=Sum(RawSQL('so_luong_con_lai * don_gia_nhap', ()))
    )
    tong_gia_tri_ton = float(gia_tri_qs['tong'] or 0)

    return Response({
        'so_san_pham': so_san_pham,
        'so_phieu_nhap': so_phieu_nhap,
        'so_phieu_xuat': so_phieu_xuat,
        'so_canh_bao': so_canh_bao,
        'tong_gia_tri_ton': tong_gia_tri_ton,
    })