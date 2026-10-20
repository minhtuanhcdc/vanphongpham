# apps/alerts/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CanhBao
from .serializers import CanhBaoSerializer


class CanhBaoViewSet(viewsets.ModelViewSet):
    queryset = CanhBao.objects.select_related('san_pham').all()
    serializer_class = CanhBaoSerializer
    filterset_fields = ['loai_canh_bao', 'da_xu_ly']

    @action(detail=True, methods=['post'])
    def xu_ly(self, request, pk=None):
        cb = self.get_object()
        cb.da_xu_ly = True
        cb.save(update_fields=['da_xu_ly'])
        return Response({'status': 'ok'})

    @action(detail=False, methods=['get'])
    def chua_xu_ly(self, request):
        qs = CanhBao.objects.filter(
            da_xu_ly=False
        ).select_related('san_pham')
        return Response(CanhBaoSerializer(qs, many=True).data)