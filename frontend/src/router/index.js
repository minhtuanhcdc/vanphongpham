import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('../layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },     // 👈 BẮT BUỘC có
    children: [
      { path: '', redirect: { name: 'dashboard' } },
      { path: 'dashboard',    name: 'dashboard',    component: () => import('../views/Dashboard.vue') },
      { path: 'khoa-phong', name: 'khoa-phong', component: () => import('../views/KhoaPhong.vue') },
      { path: 'san-pham',     name: 'san-pham',     component: () => import('../views/SanPham.vue') },
      { path: 'danh-muc',     name: 'danh-muc',     component: () => import('../views/DanhMuc.vue') },
      { path: 'nha-cung-cap', name: 'nha-cung-cap', component: () => import('../views/NhaCungCap.vue') },
      { path: 'phieu-nhap',   name: 'phieu-nhap',   component: () => import('../views/PhieuNhap.vue') },
      { path: 'phieu-xuat',   name: 'phieu-xuat',   component: () => import('../views/PhieuXuat.vue') },
      { path: 'canh-bao',     name: 'canh-bao',     component: () => import('../views/CanhBao.vue') },
      {
        path: 'tai-khoan',
        name: 'tai-khoan',
        component: () => import('../views/TaiKhoan.vue'),
        meta: { requiresAdmin: true },
      },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'login' && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { name: 'dashboard' }
  }
})

export default router