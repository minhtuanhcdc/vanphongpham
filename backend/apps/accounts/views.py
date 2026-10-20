from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import TaiKhoan
from .serializers import TaiKhoanSerializer, RegisterSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    print(">>> REQUEST DATA:", request.data)
    s = LoginSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    print(">>> VALIDATED:", s.validated_data)
    user = authenticate(
        username=s.validated_data['ten_dang_nhap'],
        password=s.validated_data['mat_khau']
    )
    print(">>> AUTH USER:", user) 
    if not user:
        return Response({'error': 'Sai tên đăng nhập hoặc mật khẩu'},
                        status=status.HTTP_401_UNAUTHORIZED)
    if not user.trang_thai:
        return Response({'error': 'Tài khoản bị khóa'},
                        status=status.HTTP_403_FORBIDDEN)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': TaiKhoanSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    s = RegisterSerializer(data=request.data)
    if s.is_valid():
        user = s.save()
        return Response(TaiKhoanSerializer(user).data, status=201)
    return Response(s.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(TaiKhoanSerializer(request.user).data)


class TaiKhoanViewSet(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all().order_by('-ma_tk')
    serializer_class = TaiKhoanSerializer