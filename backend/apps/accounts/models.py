from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class TaiKhoanManager(BaseUserManager):
    def create_user(self, ten_dang_nhap, mat_khau=None, **extra):
        if not ten_dang_nhap:
            raise ValueError('Tên đăng nhập là bắt buộc')
        user = self.model(ten_dang_nhap=ten_dang_nhap, **extra)
        user.set_password(mat_khau)
        user.save(using=self._db)
        return user

    def create_superuser(self, ten_dang_nhap, mat_khau=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('vai_tro', 'admin')
        return self.create_user(ten_dang_nhap, mat_khau, **extra)


class TaiKhoan(AbstractBaseUser, PermissionsMixin):
    VAI_TRO = [
        ('admin', 'Quản trị viên'),
        ('thukho', 'Thủ kho'),
        ('nhanvien', 'Nhân viên'),
    ]
    ma_tk = models.AutoField(primary_key=True)
    ten_dang_nhap = models.CharField(max_length=50, unique=True)
    ho_ten = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    vai_tro = models.CharField(max_length=20, choices=VAI_TRO, default='nhanvien')
    trang_thai = models.BooleanField(default=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = TaiKhoanManager()
    USERNAME_FIELD = 'ten_dang_nhap'
    REQUIRED_FIELDS = ['ho_ten']

    class Meta:
        db_table = 'tai_khoan'

    def __str__(self):
        return self.ho_ten