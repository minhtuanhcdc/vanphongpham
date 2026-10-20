# apps/inventory/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import PhieuNhap, PhieuXuat, LichSuKho
from .serializers import (
    PhieuNhapSerializer, PhieuXuatSerializer, LichSuKhoSerializer,
)
from apps.alerts.models import CanhBao
from apps.products.models import SanPham


def _tao_canh_bao_neu_chua_co(sp, loai, ton, noi_dung):
    """Tránh tạo trùng cảnh báo chưa xử lý cho cùng sản phẩm + loại."""
    exists = CanhBao.objects.filter(
        san_pham=sp, loai_canh_bao=loai, da_xu_ly=False
    ).exists()
    if not exists:
        CanhBao.objects.create(
            san_pham=sp, loai_canh_bao=loai,
            so_luong_ton=ton, noi_dung=noi_dung,
        )


class PhieuNhapViewSet(viewsets.ModelViewSet):
    queryset = PhieuNhap.objects.select_related(
        'nha_cung_cap', 'nguoi_lap'
    ).prefetch_related('chi_tiet__san_pham').all()
    serializer_class = PhieuNhapSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        chi_tiet = [
            {
                'san_pham_id': r['san_pham'].ma_sp,
                'so_luong': r['so_luong'],
                'don_gia_nhap': r.get('don_gia_nhap'),
                'han_su_dung': r.get('han_su_dung'),
            }
            for r in data['chi_tiet']
        ]

        try:
            phieu = PhieuNhap.tao_phieu(
                so_phieu=data['so_phieu'],
                nguoi_lap_id=request.user.pk,
                chi_tiet=chi_tiet,
                nha_cung_cap_id=(data['nha_cung_cap'].pk
                                 if data.get('nha_cung_cap') else None),
                so_hoa_don=data.get('so_hoa_don'),
                ghi_chu=data.get('ghi_chu'),
            )
        except ValidationError as e:
            return Response({'error': e.messages},
                            status=status.HTTP_400_BAD_REQUEST)

        # Cảnh báo tồn cao — gộp theo sản phẩm, không trùng lặp
        sp_ids = {r['san_pham_id'] for r in chi_tiet}
        for sp_id in sp_ids:
            ton = LichSuKho.ton_kho(sp_id)
            sp = SanPham.objects.get(pk=sp_id)
            if ton > sp.muc_ton_toi_da:
                _tao_canh_bao_neu_chua_co(
                    sp, 'TON_CAO', ton,
                    f'Sản phẩm {sp.ten_sp} vượt tồn tối đa ({ton}).',
                )

        return Response(
            PhieuNhapSerializer(phieu, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class PhieuXuatViewSet(viewsets.ModelViewSet):
    queryset = PhieuXuat.objects.select_related(
        'khoa_phong', 'nguoi_lap'
    ).prefetch_related('chi_tiet__san_pham').all()
    serializer_class = PhieuXuatSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        chi_tiet = [
            {
                'san_pham_id': r['san_pham'].ma_sp,
                'so_luong': r['so_luong'],
            }
            for r in data['chi_tiet']
        ]

        try:
            phieu = PhieuXuat.tao_phieu(
                so_phieu=data['so_phieu'],
                khoa_phong_id=data['khoa_phong'].pk,
                nguoi_lap_id=request.user.pk,
                chi_tiet=chi_tiet,
                nguoi_nhan=data.get('nguoi_nhan'),
                ly_do=data.get('ly_do'),
                ghi_chu=data.get('ghi_chu'),
            )
        except ValidationError as e:
            return Response({'error': e.messages},
                            status=status.HTTP_400_BAD_REQUEST)

        # Cảnh báo sắp hết / hết hàng — gộp theo sản phẩm
        sp_ids = {r['san_pham_id'] for r in chi_tiet}
        for sp_id in sp_ids:
            ton = LichSuKho.ton_kho(sp_id)
            sp = SanPham.objects.get(pk=sp_id)
            if ton == 0:
                _tao_canh_bao_neu_chua_co(
                    sp, 'HET_HANG', 0,
                    f'Sản phẩm {sp.ten_sp} đã hết hàng!',
                )
            elif ton <= sp.muc_ton_toi_thieu:
                _tao_canh_bao_neu_chua_co(
                    sp, 'SAP_HET', ton,
                    f'Sản phẩm {sp.ten_sp} sắp hết (còn {ton}).',
                )

        return Response(
            PhieuXuatSerializer(phieu, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class LichSuKhoViewSet(viewsets.ReadOnlyModelViewSet):
    """Xem lịch sử kho + tồn kho hiện tại"""
    queryset = LichSuKho.objects.select_related(
        'san_pham', 'nguoi_thuc_hien'
    ).all()
    serializer_class = LichSuKhoSerializer
    filterset_fields = ['loai', 'san_pham']

    @action(detail=False, methods=['get'])
    def ton_kho(self, request):
        return Response(LichSuKho.ton_kho_tat_ca())