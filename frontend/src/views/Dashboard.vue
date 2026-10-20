<template>
  <div class="space-y-6">
    <!-- Tiêu đề -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p class="text-sm text-gray-500 mt-1">
          Tổng quan hoạt động kho văn phòng phẩm
        </p>
      </div>
      <button
        @click="loadData"
        :disabled="loading"
        class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
               hover:bg-blue-700 transition disabled:opacity-60"
      >
        {{ loading ? 'Đang tải...' : '↻ Làm mới' }}
      </button>
    </div>

    <!-- Thẻ số liệu -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="card in stats"
        :key="card.key"
        class="bg-white rounded-xl shadow-sm p-5 border border-gray-100
               hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">{{ card.label }}</p>
            <p class="text-3xl font-bold mt-2" :class="card.color">
              {{ card.value }}
            </p>
            <p v-if="card.sub" class="text-xs text-gray-400 mt-1">
              {{ card.sub }}
            </p>
          </div>
          <div
            class="w-12 h-12 rounded-full flex items-center justify-center"
            :class="card.bg"
          >
            <component :is="card.icon" class="w-6 h-6" :class="card.color" />
          </div>
        </div>
      </div>
    </div>

    <!-- Quy trình + Cảnh báo -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Quy trình quản lý -->
      <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <h2 class="text-lg font-semibold text-gray-800 mb-5">
          🔄 Quy trình quản lý văn phòng phẩm
        </h2>
        <ol class="relative border-l-2 border-blue-200 ml-3 space-y-6">
          <li v-for="(step, i) in quyTrinh" :key="i" class="ml-6">
            <span
              class="absolute -left-4 flex items-center justify-center
                     w-8 h-8 rounded-full bg-blue-600 text-white text-sm font-bold"
            >
              {{ i + 1 }}
            </span>
            <h3 class="font-semibold text-gray-800">{{ step.title }}</h3>
            <p class="text-sm text-gray-500 mt-1">{{ step.desc }}</p>
            <span
              class="inline-block mt-2 text-xs px-2 py-0.5 rounded-full"
              :class="step.badgeClass"
            >
              {{ step.role }}
            </span>
          </li>
        </ol>
      </div>

      <!-- Cảnh báo tồn kho -->
      <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-semibold text-gray-800">
            ⚠️ Cảnh báo tồn kho
          </h2>
          <router-link
            to="/canh-bao"
            class="text-sm text-blue-600 hover:underline"
          >
            Xem tất cả →
          </router-link>
        </div>

        <div v-if="loadingCanhBao" class="text-center py-8 text-gray-400 text-sm">
          Đang tải...
        </div>
        <div
          v-else-if="canhBao.length === 0"
          class="text-center py-8 text-gray-400 text-sm"
        >
          🎉 Không có cảnh báo nào
        </div>
        <ul v-else class="space-y-3">
          <li
            v-for="(item, i) in canhBao.slice(0, 5)"
            :key="i"
            class="flex items-start gap-3 p-3 rounded-lg bg-red-50 border border-red-100"
          >
            <ExclamationTriangleIcon class="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-800 truncate">
                {{ item.ten_sp || 'Sản phẩm' }}
              </p>
              <p class="text-xs text-gray-500 truncate">
                {{ item.noi_dung || '—' }}
              </p>
            </div>
            <span
              class="text-xs font-semibold px-2 py-0.5 rounded-full whitespace-nowrap"
              :class="loaiCanhBaoClass(item.loai_canh_bao)"
            >
              {{ loaiCanhBaoLabel(item.loai_canh_bao) }}
            </span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Hoạt động gần đây -->
    <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
      <h2 class="text-lg font-semibold text-gray-800 mb-5">
        📋 Hoạt động gần đây
      </h2>
      <div v-if="loadingHoatDong" class="text-center py-6 text-gray-400 text-sm">
        Đang tải...
      </div>
      <div
        v-else-if="hoatDong.length === 0"
        class="text-center py-6 text-gray-400 text-sm"
      >
        Chưa có hoạt động nào
      </div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-gray-500 border-b border-gray-200">
              <th class="pb-3 font-medium">Loại</th>
              <th class="pb-3 font-medium">Số phiếu</th>
              <th class="pb-3 font-medium">Ngày</th>
              <th class="pb-3 font-medium">Người lập</th>
              <th class="pb-3 font-medium text-right">Tổng SL</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, i) in hoatDong"
              :key="i"
              class="border-b border-gray-50 hover:bg-gray-50"
            >
              <td class="py-3">
                <span
                  class="text-xs font-semibold px-2 py-0.5 rounded-full"
                  :class="item.loai === 'nhap'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-blue-100 text-blue-700'"
                >
                  {{ item.loai === 'nhap' ? '↓ Nhập' : '↑ Xuất' }}
                </span>
              </td>
              <td class="py-3 font-medium text-gray-700">
                {{ item.ma_phieu || '—' }}
              </td>
              <td class="py-3 text-gray-500">
                {{ formatDate(item.ngay) }}
              </td>
              <td class="py-3 text-gray-600">
                {{ item.nguoi_tao || '—' }}
              </td>
              <td class="py-3 text-right font-medium text-gray-700">
                {{ item.tong_so_luong }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/axios'
import {
  CubeIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/24/outline'

// ===== State =====
const loading = ref(false)
const loadingCanhBao = ref(false)
const loadingHoatDong = ref(false)

const soSanPham = ref(0)
const soPhieuNhap = ref(0)
const soPhieuXuat = ref(0)
const soCanhBao = ref(0)
const tongGiaTriTon = ref(0)

const canhBao = ref([])
const hoatDong = ref([])

// ===== Derived =====
const stats = computed(() => [
  {
    key: 'san-pham',
    label: 'Sản phẩm',
    value: soSanPham.value,
    sub: 'Đang quản lý',
    color: 'text-blue-600',
    bg: 'bg-blue-50',
    icon: CubeIcon,
  },
  {
    key: 'phieu-nhap',
    label: 'Phiếu nhập',
    value: soPhieuNhap.value,
    sub: 'Tổng số phiếu',
    color: 'text-green-600',
    bg: 'bg-green-50',
    icon: ArrowDownTrayIcon,
  },
  {
    key: 'phieu-xuat',
    label: 'Phiếu xuất',
    value: soPhieuXuat.value,
    sub: 'Tổng số phiếu',
    color: 'text-orange-600',
    bg: 'bg-orange-50',
    icon: ArrowUpTrayIcon,
  },
  {
    key: 'canh-bao',
    label: 'Cảnh báo',
    value: soCanhBao.value,
    sub: 'Chưa xử lý',
    color: 'text-red-600',
    bg: 'bg-red-50',
    icon: ExclamationTriangleIcon,
  },
])

const quyTrinh = [
  {
    title: 'Tiếp nhận nhu cầu',
    desc: 'Các phòng ban gửi yêu cầu cấp phát văn phòng phẩm.',
    role: 'Phòng ban',
    badgeClass: 'bg-gray-100 text-gray-600',
  },
  {
    title: 'Lập phiếu nhập',
    desc: 'Kho tạo phiếu nhập khi nhận hàng từ nhà cung cấp.',
    role: 'Thủ kho',
    badgeClass: 'bg-green-100 text-green-700',
  },
  {
    title: 'Kiểm tra & nhập kho',
    desc: 'Kiểm tra số lượng, chất lượng và cập nhật tồn kho.',
    role: 'Thủ kho',
    badgeClass: 'bg-green-100 text-green-700',
  },
  {
    title: 'Cấp phát / Xuất kho',
    desc: 'Lập phiếu xuất khi cấp phát cho phòng ban sử dụng.',
    role: 'Thủ kho',
    badgeClass: 'bg-blue-100 text-blue-700',
  },
  {
    title: 'Theo dõi tồn kho',
    desc: 'Hệ thống tự động cảnh báo khi tồn dưới ngưỡng tối thiểu.',
    role: 'Hệ thống',
    badgeClass: 'bg-purple-100 text-purple-700',
  },
  {
    title: 'Báo cáo & xử lý',
    desc: 'Quản trị viên xem báo cáo, xử lý cảnh báo và lập kế hoạch.',
    role: 'Quản trị viên',
    badgeClass: 'bg-amber-100 text-amber-700',
  },
]

// ===== Helpers =====
function formatDate(d) {
  if (!d) return '—'
  try {
    return new Date(d).toLocaleDateString('vi-VN')
  } catch {
    return d
  }
}

function loaiCanhBaoClass(loai) {
  switch (loai) {
    case 'HET_HANG': return 'bg-red-500 text-white'
    case 'SAP_HET':  return 'bg-amber-500 text-white'
    case 'TON_CAO':  return 'bg-blue-500 text-white'
    default:         return 'bg-gray-400 text-white'
  }
}

function loaiCanhBaoLabel(loai) {
  switch (loai) {
    case 'HET_HANG': return 'Hết hàng'
    case 'SAP_HET':  return 'Sắp hết'
    case 'TON_CAO':  return 'Tồn cao'
    default:         return loai || '—'
  }
}

// ===== Data loaders =====
async function loadStats() {
  try {
    const { data } = await api.get('/dashboard/thong-ke/')
    soSanPham.value     = data.so_san_pham     ?? 0
    soPhieuNhap.value   = data.so_phieu_nhap   ?? 0
    soPhieuXuat.value   = data.so_phieu_xuat   ?? 0
    soCanhBao.value     = data.so_canh_bao     ?? 0
    tongGiaTriTon.value = data.tong_gia_tri_ton ?? 0
  } catch {
    // Fallback: gọi đúng endpoint thực tế
    await Promise.allSettled([
      api.get('/products/san-pham/').then(r => {
        const list = r.data?.results ?? r.data ?? []
        soSanPham.value = list.length
      }),
      api.get('/inventory/phieu-nhap/').then(r => {
        const list = r.data?.results ?? r.data ?? []
        soPhieuNhap.value = list.length
      }),
      api.get('/inventory/phieu-xuat/').then(r => {
        const list = r.data?.results ?? r.data ?? []
        soPhieuXuat.value = list.length
      }),
    ])
  }
}

async function loadCanhBao() {
  loadingCanhBao.value = true
  try {
    const { data } = await api.get('/alerts/canh-bao/chua_xu_ly/')
    const list = data?.results ?? data ?? []
    canhBao.value = list
    soCanhBao.value = list.length
  } catch {
    canhBao.value = []
  } finally {
    loadingCanhBao.value = false
  }
}

async function loadHoatDong() {
  loadingHoatDong.value = true
  try {
    const [nhap, xuat] = await Promise.allSettled([
      api.get('/inventory/phieu-nhap/'),
      api.get('/inventory/phieu-xuat/'),
    ])

    const listNhap = (nhap.value?.data?.results ?? nhap.value?.data ?? []).map(x => ({
      loai: 'nhap',
      ma_phieu: x.so_phieu,
      ngay: x.ngay_nhap,
      nguoi_tao: x.ten_nguoi_lap,
      tong_so_luong: (x.chi_tiet || []).reduce(
        (s, ct) => s + (Number(ct.so_luong) || 0), 0
      ),
    }))

    const listXuat = (xuat.value?.data?.results ?? xuat.value?.data ?? []).map(x => ({
      loai: 'xuat',
      ma_phieu: x.so_phieu,
      ngay: x.ngay_xuat,
      nguoi_tao: x.ten_nguoi_lap,
      tong_so_luong: (x.chi_tiet || []).reduce(
        (s, ct) => s + (Number(ct.so_luong) || 0), 0
      ),
    }))

    hoatDong.value = [...listNhap, ...listXuat]
      .sort((a, b) => new Date(b.ngay || 0) - new Date(a.ngay || 0))
      .slice(0, 8)
  } catch {
    hoatDong.value = []
  } finally {
    loadingHoatDong.value = false
  }
}

async function loadData() {
  loading.value = true
  await Promise.allSettled([loadStats(), loadCanhBao(), loadHoatDong()])
  loading.value = false
}

onMounted(loadData)
</script>