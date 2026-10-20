<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" class="aside">
      <div class="logo">📦 Kho VPP</div>
      <el-menu :default-active="$route.path" router background-color="#1f2d3d" text-color="#bfcbd9" active-text-color="#409eff">
        <el-menu-item index="/dashboard"><el-icon><HomeFilled /></el-icon>Dashboard</el-menu-item>
        <el-menu-item index="/san-pham"><el-icon><Goods /></el-icon>Sản phẩm</el-menu-item>
        <el-menu-item index="/danh-muc"><el-icon><Menu /></el-icon>Danh mục</el-menu-item>
        <el-menu-item index="/nha-cung-cap"><el-icon><Shop /></el-icon>Nhà cung cấp</el-menu-item>
        <el-menu-item index="/phieu-nhap"><el-icon><Download /></el-icon>Phiếu nhập</el-menu-item>
        <el-menu-item index="/phieu-xuat"><el-icon><Upload /></el-icon>Phiếu xuất</el-menu-item>
        <el-menu-item index="/canh-bao">
          <el-icon><WarningFilled /></el-icon>Cảnh báo
          <el-badge v-if="soCanhBao > 0" :value="soCanhBao" style="margin-left:8px" />
        </el-menu-item>
        <el-menu-item v-if="auth.isAdmin" index="/tai-khoan"><el-icon><UserFilled /></el-icon>Tài khoản</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div></div>
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon> {{ auth.user?.ho_ten }}
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">Đăng xuất</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main style="background:#f0f2f5">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const auth = useAuthStore()
const router = useRouter()
const soCanhBao = ref(0)

const handleCommand = (cmd) => {
  if (cmd === 'logout') {
    auth.logout()
    router.push('/login')
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get('/alerts/canh-bao/chua_xu_ly/')
    soCanhBao.value = data.length
  } catch {}
})
</script>

<style scoped>
.aside { background: #1f2d3d; }
.logo { color: #fff; font-size: 20px; font-weight: bold; padding: 20px; text-align: center; }
.header { background: #fff; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
.user-info { cursor: pointer; display: flex; align-items: center; gap: 6px; }
</style>