from rest_framework import serializers
from .models import TaiKhoan


class TaiKhoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = ['ma_tk', 'ten_dang_nhap', 'ho_ten', 'email',
                  'vai_tro', 'trang_thai', 'ngay_tao']
        read_only_fields = ['ma_tk', 'ngay_tao']


class RegisterSerializer(serializers.ModelSerializer):
    mat_khau = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = TaiKhoan
        fields = ['ten_dang_nhap', 'mat_khau', 'ho_ten', 'email', 'vai_tro']

    def create(self, data):
        return TaiKhoan.objects.create_user(
            ten_dang_nhap=data['ten_dang_nhap'],
            mat_khau=data['mat_khau'],
            ho_ten=data['ho_ten'],
            email=data.get('email', ''),
            vai_tro=data.get('vai_tro', 'nhanvien')
        )


class LoginSerializer(serializers.Serializer):
    ten_dang_nhap = serializers.CharField()
    mat_khau = serializers.CharField()