<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-60 bg-slate-800 flex flex-col shrink-0">
      <div class="text-white text-xl font-bold py-5 text-center tracking-wide">
        📦 Kho VPP
      </div>

      <nav class="flex-1 overflow-y-auto px-2 space-y-1">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg text-slate-300
                 hover:bg-slate-700 hover:text-white transition-colors"
          :class="{ 'bg-blue-600 !text-white': $route.path === item.path }"
        >
          <component :is="item.icon" class="w-5 h-5 shrink-0" />
          <span class="flex-1">{{ item.label }}</span>

          <!-- Badge cảnh báo -->
          <span
            v-if="item.path === '/canh-bao' && soCanhBao > 0"
            class="bg-red-500 text-white text-xs font-bold rounded-full
                   min-w-5 h-5 flex items-center justify-center px-1.5"
          >
            {{ soCanhBao > 99 ? '99+' : soCanhBao }}
          </span>
        </router-link>
      </nav>
    </aside>

    <!-- Main -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Header -->
      <header
        class="h-14 bg-white flex items-center justify-end px-6
               shadow-sm sticky top-0 z-10"
      >
        <div class="relative" ref="dropdownRef">
          <button
            @click="openDropdown = !openDropdown"
            class="flex items-center gap-2 px-3 py-1.5 rounded-lg
                   hover:bg-gray-100 transition-colors text-gray-700"
          >
            <UserIcon class="w-5 h-5" />
            <span class="font-medium">{{ auth.user?.ho_ten }}</span>
            <ChevronDownIcon class="w-4 h-4" />
          </button>

          <transition
            enter-active-class="transition ease-out duration-150"
            enter-from-class="opacity-0 -translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-100"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-1"
          >
            <div
              v-if="openDropdown"
              class="absolute right-0 mt-2 w-44 bg-white rounded-lg shadow-lg
                     border border-gray-100 py-1 z-20"
            >
              <button
                @click="handleLogout"
                class="w-full text-left px-4 py-2 text-sm text-gray-700
                       hover:bg-gray-100 flex items-center gap-2"
              >
                <ArrowRightOnRectangleIcon class="w-4 h-4" />
                Đăng xuất
              </button>
            </div>
          </transition>
        </div>
      </header>

      <!-- Content -->
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api/axios'
import { BuildingOfficeIcon } from '@heroicons/vue/24/outline'

// Heroicons (outline) — dùng thư viện @heroicons/vue
import {
  HomeIcon,
  CubeIcon,
  Bars3Icon,
  BuildingStorefrontIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  ExclamationTriangleIcon,
  UsersIcon,
  UserIcon,
  ChevronDownIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const router = useRouter()
const soCanhBao = ref(0)
const openDropdown = ref(false)
const dropdownRef = ref(null)

const menuItems = computed(() => {
  const items = [
    { path: '/dashboard', label: 'Dashboard', icon: HomeIcon },
    { path: '/khoa-phong', label: 'Khoa/Phòng', icon: BuildingOfficeIcon }, 
    { path: '/san-pham', label: 'Sản phẩm', icon: CubeIcon },
    { path: '/danh-muc', label: 'Danh mục', icon: Bars3Icon },
    { path: '/nha-cung-cap', label: 'Nhà cung cấp', icon: BuildingStorefrontIcon },
    { path: '/phieu-nhap', label: 'Phiếu nhập', icon: ArrowDownTrayIcon },
    { path: '/phieu-xuat', label: 'Phiếu xuất', icon: ArrowUpTrayIcon },
    { path: '/canh-bao', label: 'Cảnh báo', icon: ExclamationTriangleIcon },
  ]
  if (auth.isAdmin) {
    items.push({ path: '/tai-khoan', label: 'Tài khoản', icon: UsersIcon })
  }
  return items
})

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}

// Đóng dropdown khi click ra ngoài
const handleClickOutside = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    openDropdown.value = false
  }
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  try {
    const { data } = await api.get('/alerts/canh-bao/chua_xu_ly/')
    soCanhBao.value = data.length
  } catch {}
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>