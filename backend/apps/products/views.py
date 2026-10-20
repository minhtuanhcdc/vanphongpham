# apps/products/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from .models import DanhMuc, NhaCungCap, SanPham
from .serializers import (
    DanhMucSerializer, NhaCungCapSerializer, SanPhamSerializer,
)
from apps.inventory.models import ChiTietPhieuNhap, ChiTietPhieuXuat


def _build_ton_map():
    rows = (
        ChiTietPhieuNhap.objects
        .filter(phieu_nhap__trang_thai='NHAP')
        .values('san_pham_id')
        .annotate(tong=Sum('so_luong_con_lai'))
    )
    return {r['san_pham_id']: (r['tong'] or 0) for r in rows}


def _build_nhap_map():
    rows = (
        ChiTietPhieuNhap.objects
        .filter(phieu_nhap__trang_thai='NHAP')
        .values('san_pham_id')
        .annotate(tong=Sum('so_luong'))
    )
    return {r['san_pham_id']: (r['tong'] or 0) for r in rows}


def _build_xuat_map():
    rows = (
        ChiTietPhieuXuat.objects
        .filter(phieu_xuat__trang_thai='XUAT')
        .values('san_pham_id')
        .annotate(tong=Sum('so_luong'))
    )
    return {r['san_pham_id']: (r['tong'] or 0) for r in rows}


class DanhMucViewSet(viewsets.ModelViewSet):
    queryset = DanhMuc.objects.all()
    serializer_class = DanhMucSerializer
    search_fields = ['ten_dm']


class NhaCungCapViewSet(viewsets.ModelViewSet):
    queryset = NhaCungCap.objects.all()
    serializer_class = NhaCungCapSerializer
    search_fields = ['ten_ncc', 'dien_thoai']


class SanPhamViewSet(viewsets.ModelViewSet):
    queryset = SanPham.objects.select_related('danh_muc').all()
    serializer_class = SanPhamSerializer
    search_fields = ['ten_sp']
    filterset_fields = ['danh_muc', 'trang_thai']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        if self.action in ('list', 'retrieve', 'canh_bao'):
            ctx['ton_map'] = _build_ton_map()
            ctx['nhap_map'] = _build_nhap_map()
            ctx['xuat_map'] = _build_xuat_map()
        return ctx

    @action(detail=False, methods=['get'])
    def canh_bao(self, request):
        ton_map = _build_ton_map()
        qs = SanPham.objects.filter(trang_thai=True).select_related('danh_muc')

        het_hang, sap_het, ton_cao = [], [], []
        for sp in qs:
            ton = ton_map.get(sp.ma_sp, 0)
            if ton == 0:
                het_hang.append(sp)
            elif ton <= sp.muc_ton_toi_thieu:
                sap_het.append(sp)
            elif ton > sp.muc_ton_toi_da:
                ton_cao.append(sp)

        ctx = {
            'ton_map': ton_map,
            'nhap_map': _build_nhap_map(),
            'xuat_map': _build_xuat_map(),
        }
        return Response({
            'het_hang': SanPhamSerializer(het_hang, many=True, context=ctx).data,
            'sap_het': SanPhamSerializer(sap_het, many=True, context=ctx).data,
            'ton_cao': SanPhamSerializer(ton_cao, many=True, context=ctx).data,
        })