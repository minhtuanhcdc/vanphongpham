<template>
  <div class="space-y-5">
    <!-- Tiêu đề + nút thêm -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Phiếu xuất kho</h1>
        <p class="text-sm text-gray-500 mt-1">
          Cấp phát văn phòng phẩm cho các khoa/phòng
        </p>
      </div>
      <button
        @click="openCreate"
        class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
               hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="w-4 h-4" /> Lập phiếu xuất
      </button>
    </div>

    <!-- Toast -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="toast.show"
        class="fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg text-sm text-white"
        :class="toast.type === 'success' ? 'bg-green-600' : 'bg-red-600'"
      >
        {{ toast.message }}
      </div>
    </transition>

    <!-- Bộ lọc -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
        <div class="relative sm:col-span-2">
          <MagnifyingGlassIcon
            class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2"
          />
          <input
            v-model="search"
            type="text"
            placeholder="Tìm theo số phiếu, khoa phòng, người nhận..."
            class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm
                   outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>
        <select
          v-model="filterKhoaPhong"
          class="px-3 py-2 border border-gray-300 rounded-lg text-sm
                 outline-none focus:border-blue-500"
        >
          <option value="">Tất cả khoa phòng</option>
          <option v-for="kp in khoaPhongList" :key="kp.ma_kp" :value="kp.ma_kp">
            {{ kp.ten_kp }}
          </option>
        </select>
        <select
          v-model="filterTrangThai"
          class="px-3 py-2 border border-gray-300 rounded-lg text-sm
                 outline-none focus:border-blue-500"
        >
          <option value="">Tất cả trạng thái</option>
          <option value="XUAT">Đã xuất</option>
          <option value="HUY">Đã hủy</option>
        </select>
      </div>
    </div>

    <!-- Bảng -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div v-if="loading" class="text-center py-12 text-gray-400 text-sm">
        Đang tải dữ liệu...
      </div>

      <div
        v-else-if="filteredList.length === 0"
        class="text-center py-12 text-gray-400 text-sm"
      >
        <p class="text-4xl mb-2">📤</p>
        Chưa có phiếu xuất nào
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr class="text-left text-gray-600">
              <th class="px-4 py-3 font-medium w-16">Mã</th>
              <th class="px-4 py-3 font-medium">Số phiếu</th>
              <th class="px-4 py-3 font-medium">Khoa phòng</th>
              <th class="px-4 py-3 font-medium">Người nhận</th>
              <th class="px-4 py-3 font-medium">Ngày xuất</th>
              <th class="px-4 py-3 font-medium text-center">Số mặt hàng</th>
              <th class="px-4 py-3 font-medium text-center">Tổng SL xuất</th>
              <th class="px-4 py-3 font-medium text-center">Trạng thái</th>
              <th class="px-4 py-3 font-medium text-right w-32">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedList"
              :key="item.ma_px"
              class="border-b border-gray-50 hover:bg-gray-50 transition-colors"
            >
              <td class="px-4 py-3 font-mono text-xs text-gray-500">
                {{ item.ma_px }}
              </td>
              <td class="px-4 py-3 font-medium text-gray-800">
                {{ item.so_phieu }}
              </td>
              <td class="px-4 py-3 text-gray-700">
                {{ item.ten_kp || '—' }}
              </td>
              <td class="px-4 py-3 text-gray-600">
                {{ item.nguoi_nhan || '—' }}
              </td>
              <td class="px-4 py-3 text-gray-600">
                {{ formatDate(item.ngay_xuat) }}
              </td>
              <td class="px-4 py-3 text-center">
                <span class="text-xs font-semibold px-2 py-1 rounded-full bg-blue-100 text-blue-700">
                  {{ item.chi_tiet?.length ?? 0 }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span class="text-xs font-semibold px-2 py-1 rounded-full bg-indigo-100 text-indigo-700">
                  {{ tongSoLuongPhieu(item) }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full"
                  :class="item.trang_thai === 'XUAT'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-500'"
                >
                  {{ item.trang_thai === 'XUAT' ? 'Đã xuất' : 'Đã hủy' }}
                </span>
              </td>
              <td class="px-4 py-3 text-right whitespace-nowrap">
                <button
                  @click="openDetail(item)"
                  class="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                  title="Xem chi tiết"
                >
                  <EyeIcon class="w-4 h-4" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Phân trang -->
      <div
        v-if="!loading && filteredList.length > 0"
        class="px-4 py-3 bg-gray-50 border-t border-gray-200
               flex flex-col sm:flex-row items-center justify-between gap-2 text-sm"
      >
        <span class="text-gray-500">
          Hiển thị {{ (page - 1) * pageSize + 1 }}–{{
            Math.min(page * pageSize, filteredList.length)
          }} / {{ filteredList.length }}
        </span>
        <div class="flex items-center gap-1">
          <button
            @click="page > 1 && page--"
            :disabled="page === 1"
            class="px-3 py-1.5 rounded-lg border border-gray-300 bg-white
                   hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            ‹ Trước
          </button>
          <span class="px-3 text-gray-600">Trang {{ page }} / {{ totalPages }}</span>
          <button
            @click="page < totalPages && page++"
            :disabled="page >= totalPages"
            class="px-3 py-1.5 rounded-lg border border-gray-300 bg-white
                   hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Sau ›
          </button>
        </div>
      </div>
    </div>

    <!-- ===== MODAL TẠO PHIẾU XUẤT ===== -->
    <teleport to="body">
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="showFormModal"
          class="fixed inset-0 z-40 bg-black/40 flex items-center justify-center p-4"
          @click.self="closeFormModal"
        >
          <div class="bg-white rounded-xl shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-800">Lập phiếu xuất kho</h3>
              <button
                @click="closeFormModal"
                class="p-1.5 text-gray-400 hover:bg-gray-100 rounded-lg"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
              <!-- Thông tin phiếu -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Số phiếu <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.so_phieu"
                    type="text"
                    placeholder="VD: PX-2026-001"
                    class="w-full px-3 py-2 border rounded-lg text-sm outline-none
                           focus:ring-1 focus:ring-blue-500"
                    :class="errors.so_phieu ? 'border-red-400' : 'border-gray-300 focus:border-blue-500'"
                  />
                  <p v-if="errors.so_phieu" class="text-xs text-red-600 mt-1">
                    {{ errors.so_phieu }}
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Khoa phòng nhận <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.khoa_phong"
                    class="w-full px-3 py-2 border rounded-lg text-sm outline-none
                           focus:ring-1 focus:ring-blue-500"
                    :class="errors.khoa_phong ? 'border-red-400' : 'border-gray-300 focus:border-blue-500'"
                  >
                    <option :value="null">-- Chọn khoa phòng --</option>
                    <option v-for="kp in khoaPhongList" :key="kp.ma_kp" :value="kp.ma_kp">
                      {{ kp.ten_kp }}
                    </option>
                  </select>
                  <p v-if="errors.khoa_phong" class="text-xs text-red-600 mt-1">
                    {{ errors.khoa_phong }}
                  </p>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Người nhận
                  </label>
                  <input
                    v-model="form.nguoi_nhan"
                    type="text"
                    placeholder="Họ tên người đại diện nhận hàng"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Lý do xuất
                  </label>
                  <input
                    v-model="form.ly_do"
                    type="text"
                    placeholder="VD: Cấp phát định kỳ tháng 10"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Ghi chú
                </label>
                <input
                  v-model="form.ghi_chu"
                  type="text"
                  placeholder="Ghi chú thêm..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                         outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <!-- Chi tiết phiếu -->
              <div class="border-t border-gray-200 pt-4">
                <div class="flex items-center justify-between mb-3">
                  <h4 class="text-sm font-semibold text-gray-700">
                    Mặt hàng xuất <span class="text-red-500">*</span>
                  </h4>
                  <button
                    type="button"
                    @click="addChiTiet"
                    class="px-3 py-1.5 text-xs bg-blue-50 text-blue-700 rounded-lg
                           hover:bg-blue-100 transition flex items-center gap-1"
                  >
                    <PlusIcon class="w-3 h-3" /> Thêm dòng
                  </button>
                </div>

                <div
                  v-if="form.chi_tiet.length === 0"
                  class="text-center py-6 text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-lg"
                >
                  Chưa có mặt hàng nào. Nhấn "Thêm dòng" để bắt đầu.
                </div>

                <div v-else class="space-y-2">
                  <div
                    v-for="(row, idx) in form.chi_tiet"
                    :key="idx"
                    class="bg-gray-50 rounded-lg p-3"
                  >
                    <div class="grid grid-cols-12 gap-2 items-start">
                      <div class="col-span-12 sm:col-span-6">
                        <label class="block text-xs text-gray-500 mb-1">Sản phẩm</label>
                        <select
                          v-model="row.san_pham"
                          class="w-full px-2 py-1.5 border rounded text-sm
                                 outline-none focus:border-blue-500"
                          :class="rowErrors[idx]?.san_pham ? 'border-red-400' : 'border-gray-300'"
                        >
                          <option :value="null">-- Chọn sản phẩm --</option>
                          <option
                            v-for="sp in sanPhamList"
                            :key="sp.ma_sp"
                            :value="sp.ma_sp"
                          >
                            {{ sp.ten_sp }} (Tồn: {{ sp.so_luong_ton ?? 0 }} {{ sp.don_vi_tinh || '' }})
                          </option>
                        </select>
                        <p v-if="rowErrors[idx]?.san_pham" class="text-xs text-red-600 mt-1">
                          {{ rowErrors[idx].san_pham }}
                        </p>
                      </div>
                      <div class="col-span-6 sm:col-span-3">
                        <label class="block text-xs text-gray-500 mb-1">Số lượng xuất</label>
                        <input
                          v-model.number="row.so_luong"
                          type="number"
                          min="1"
                          class="w-full px-2 py-1.5 border rounded text-sm
                                 outline-none focus:border-blue-500"
                          :class="rowErrors[idx]?.so_luong ? 'border-red-400' : 'border-gray-300'"
                        />
                        <p v-if="rowErrors[idx]?.so_luong" class="text-xs text-red-600 mt-1">
                          {{ rowErrors[idx].so_luong }}
                        </p>
                      </div>
                      <div class="col-span-5 sm:col-span-2">
                        <label class="block text-xs text-gray-500 mb-1">Tồn hiện tại</label>
                        <div class="px-2 py-1.5 bg-white border border-gray-200 rounded text-sm">
                          <span
                            class="font-semibold"
                            :class="tonSau(row) < 0 ? 'text-red-600' : 'text-gray-700'"
                          >
                            {{ tonCuaSanPham(row.san_pham) }}
                          </span>
                        </div>
                      </div>
                      <div class="col-span-1 flex justify-end pt-6">
                        <button
                          type="button"
                          @click="removeChiTiet(idx)"
                          class="p-1.5 text-red-600 hover:bg-red-100 rounded transition"
                          title="Xóa dòng"
                        >
                          <TrashIcon class="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    <p
                      v-if="row.san_pham && tonSau(row) < 0"
                      class="text-xs text-red-600 mt-2 font-medium"
                    >
                      ⚠ Vượt tồn kho! Số lượng xuất ({{ row.so_luong }}) lớn hơn tồn hiện tại ({{ tonCuaSanPham(row.san_pham) }}).
                    </p>
                  </div>
                </div>
              </div>

              <!-- Tổng kết -->
              <div
                v-if="form.chi_tiet.length > 0"
                class="bg-blue-50 rounded-lg p-3 text-sm"
              >
                <div class="flex justify-between">
                  <span class="text-gray-600">Tổng số mặt hàng:</span>
                  <span class="font-semibold">{{ form.chi_tiet.length }}</span>
                </div>
                <div class="flex justify-between mt-1">
                  <span class="text-gray-600">Tổng số lượng xuất:</span>
                  <span class="font-semibold">{{ tongSoLuong }}</span>
                </div>
              </div>

              <p
                v-if="formError"
                class="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg"
              >
                {{ formError }}
              </p>

              <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
                <button
                  type="button"
                  @click="closeFormModal"
                  class="px-4 py-2 text-sm border border-gray-300 rounded-lg
                         hover:bg-gray-50 transition"
                >
                  Huỷ
                </button>
                <button
                  type="submit"
                  :disabled="submitting || coDongVuotTon"
                  class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
                         hover:bg-blue-700 transition disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  {{ submitting ? 'Đang lưu...' : 'Lưu phiếu xuất' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- ===== MODAL CHI TIẾT ===== -->
    <teleport to="body">
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="showDetailModal"
          class="fixed inset-0 z-40 bg-black/40 flex items-center justify-center p-4"
          @click.self="showDetailModal = false"
        >
          <div class="bg-white rounded-xl shadow-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-800">
                Chi tiết phiếu {{ detailItem?.so_phieu }}
              </h3>
              <button
                @click="showDetailModal = false"
                class="p-1.5 text-gray-400 hover:bg-gray-100 rounded-lg"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>

            <div v-if="detailItem" class="p-6 space-y-4">
              <div class="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <span class="text-gray-500">Số phiếu:</span>
                  <span class="font-medium ml-2">{{ detailItem.so_phieu }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Ngày xuất:</span>
                  <span class="font-medium ml-2">{{ formatDate(detailItem.ngay_xuat) }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Khoa phòng:</span>
                  <span class="font-medium ml-2">{{ detailItem.ten_kp || '—' }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Người nhận:</span>
                  <span class="font-medium ml-2">{{ detailItem.nguoi_nhan || '—' }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Người lập:</span>
                  <span class="font-medium ml-2">{{ detailItem.ten_nguoi_lap || '—' }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Trạng thái:</span>
                  <span
                    class="text-xs font-semibold px-2 py-0.5 rounded-full ml-2"
                    :class="detailItem.trang_thai === 'XUAT'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-500'"
                  >
                    {{ detailItem.trang_thai === 'XUAT' ? 'Đã xuất' : 'Đã hủy' }}
                  </span>
                </div>
                <div v-if="detailItem.ly_do" class="col-span-2">
                  <span class="text-gray-500">Lý do:</span>
                  <span class="font-medium ml-2">{{ detailItem.ly_do }}</span>
                </div>
              </div>

              <p v-if="detailItem.ghi_chu" class="text-sm text-gray-600 italic">
                Ghi chú: {{ detailItem.ghi_chu }}
              </p>

              <div class="border border-gray-200 rounded-lg overflow-hidden">
                <table class="w-full text-sm">
                  <thead class="bg-gray-50 border-b border-gray-200">
                    <tr class="text-left text-gray-600">
                      <th class="px-3 py-2 font-medium">Sản phẩm</th>
                      <th class="px-3 py-2 font-medium text-right">Số lượng xuất</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="ct in detailItem.chi_tiet"
                      :key="ct.id"
                      class="border-b border-gray-100"
                    >
                      <td class="px-3 py-2">{{ ct.ten_sp }}</td>
                      <td class="px-3 py-2 text-right font-medium">{{ ct.so_luong }}</td>
                    </tr>
                  </tbody>
                  <tfoot class="bg-gray-50 border-t border-gray-200">
                    <tr>
                      <td class="px-3 py-2 text-right font-semibold">Tổng cộng:</td>
                      <td class="px-3 py-2 text-right font-bold text-blue-700">
                        {{ tongSoLuongPhieu(detailItem) }}
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>

            <div class="px-6 py-4 border-t border-gray-200 flex justify-end gap-2">
              <button
                @click="printPhieu(detailItem)"
                class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
                       hover:bg-blue-700 transition flex items-center gap-2"
              >
                <PrinterIcon class="w-4 h-4" /> In phiếu
              </button>
              <button
                @click="showDetailModal = false"
                class="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import api from '@/api/axios'
import {
  PlusIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  EyeIcon,
  PrinterIcon,
} from '@heroicons/vue/24/outline'

// ===== Endpoints =====
const EP_PHIEU_XUAT = '/inventory/phieu-xuat/'
const EP_KHOA_PHONG = '/departments/khoa-phong/'
const EP_SAN_PHAM   = '/products/san-pham/'

// ===== State =====
const list = ref([])
const khoaPhongList = ref([])
const sanPhamList = ref([])

const loading = ref(false)
const submitting = ref(false)

const search = ref('')
const filterKhoaPhong = ref('')
const filterTrangThai = ref('')
const page = ref(1)
const pageSize = 10

const showFormModal = ref(false)
const showDetailModal = ref(false)
const detailItem = ref(null)
const formError = ref('')

const toast = reactive({ show: false, message: '', type: 'success' })
let toastTimer = null

const form = reactive({
  so_phieu: '',
  khoa_phong: null,
  nguoi_nhan: '',
  ly_do: '',
  ghi_chu: '',
  chi_tiet: [],
})

const errors = reactive({ so_phieu: '', khoa_phong: '' })
const rowErrors = ref([])

// ===== Computed =====
const filteredList = computed(() => {
  const kw = search.value.trim().toLowerCase()
  return list.value.filter((it) => {
    if (filterKhoaPhong.value && it.khoa_phong !== filterKhoaPhong.value) return false
    if (filterTrangThai.value && it.trang_thai !== filterTrangThai.value) return false
    if (!kw) return true
    return [it.so_phieu, it.ten_kp, it.nguoi_nhan, it.ly_do]
      .filter(Boolean)
      .some((v) => String(v).toLowerCase().includes(kw))
  })
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredList.value.length / pageSize))
)

const paginatedList = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredList.value.slice(start, start + pageSize)
})

const tongSoLuong = computed(() =>
  form.chi_tiet.reduce((s, r) => s + (Number(r.so_luong) || 0), 0)
)

const coDongVuotTon = computed(() =>
  form.chi_tiet.some((r) => r.san_pham && tonSau(r) < 0)
)

watch([search, filterKhoaPhong, filterTrangThai], () => { page.value = 1 })
watch(totalPages, (tp) => { if (page.value > tp) page.value = tp })

// ===== Helpers =====
function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('vi-VN')
}

function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toast.show = false), 2500)
}

function tongSoLuongPhieu(item) {
  if (!item?.chi_tiet) return 0
  return item.chi_tiet.reduce(
    (s, ct) => s + (Number(ct.so_luong) || 0),
    0
  )
}

function tonCuaSanPham(ma_sp) {
  if (!ma_sp) return 0
  const sp = sanPhamList.value.find((x) => x.ma_sp === ma_sp)
  return Number(sp?.so_luong_ton) || 0
}

function tonSau(row) {
  return tonCuaSanPham(row.san_pham) - (Number(row.so_luong) || 0)
}

function resetForm() {
  Object.assign(form, {
    so_phieu: '',
    khoa_phong: null,
    nguoi_nhan: '',
    ly_do: '',
    ghi_chu: '',
    chi_tiet: [],
  })
  Object.keys(errors).forEach((k) => (errors[k] = ''))
  rowErrors.value = []
  formError.value = ''
}

function validateForm() {
  errors.so_phieu = form.so_phieu.trim() ? '' : 'Vui lòng nhập số phiếu'
  errors.khoa_phong = form.khoa_phong ? '' : 'Vui lòng chọn khoa phòng'

  rowErrors.value = form.chi_tiet.map((r) => {
    const e = {}
    if (!r.san_pham) e.san_pham = 'Chọn sản phẩm'
    if (!r.so_luong || r.so_luong <= 0) {
      e.so_luong = 'SL > 0'
    } else if (r.san_pham && tonSau(r) < 0) {
      e.so_luong = `Vượt tồn (còn ${tonCuaSanPham(r.san_pham)})`
    }
    return e
  })

  const hasRowErr = rowErrors.value.some((e) => Object.keys(e).length > 0)

  if (form.chi_tiet.length === 0) {
    formError.value = 'Vui lòng thêm ít nhất 1 mặt hàng'
    return false
  }

  const tongTheoSp = {}
  form.chi_tiet.forEach((r) => {
    if (r.san_pham) {
      tongTheoSp[r.san_pham] = (tongTheoSp[r.san_pham] || 0) + (Number(r.so_luong) || 0)
    }
  })
  for (const [spId, tong] of Object.entries(tongTheoSp)) {
    if (tong > tonCuaSanPham(Number(spId))) {
      formError.value = `Sản phẩm id=${spId}: tổng xuất (${tong}) vượt tồn (${tonCuaSanPham(Number(spId))})`
      return false
    }
  }

  return !errors.so_phieu && !errors.khoa_phong && !hasRowErr
}

// ===== API =====
async function loadList() {
  loading.value = true
  try {
    const { data } = await api.get(EP_PHIEU_XUAT)
    list.value = data?.results ?? data ?? []
  } catch (e) {
    console.error('loadList:', e.response?.status, e.response?.data)
    showToast('Không tải được danh sách phiếu xuất', 'error')
    list.value = []
  } finally {
    loading.value = false
  }
}

async function loadKhoaPhong() {
  try {
    const { data } = await api.get(EP_KHOA_PHONG)
    khoaPhongList.value = data?.results ?? data ?? []
  } catch {
    khoaPhongList.value = []
  }
}

async function loadSanPham() {
  try {
    const { data } = await api.get(EP_SAN_PHAM)
    sanPhamList.value = data?.results ?? data ?? []
  } catch {
    sanPhamList.value = []
  }
}

// ===== Handlers =====
function openCreate() {
  resetForm()
  const now = new Date()
  const ymd = now.toISOString().slice(0, 10).replace(/-/g, '')
  const rand = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  form.so_phieu = `PX-${ymd}-${rand}`
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  formError.value = ''
}

function addChiTiet() {
  form.chi_tiet.push({
    san_pham: null,
    so_luong: 1,
  })
  rowErrors.value.push({})
}

function removeChiTiet(idx) {
  form.chi_tiet.splice(idx, 1)
  rowErrors.value.splice(idx, 1)
}

async function handleSubmit() {
  if (!validateForm()) return
  submitting.value = true
  formError.value = ''
  try {
    const payload = {
      so_phieu: form.so_phieu,
      khoa_phong: form.khoa_phong,
      nguoi_nhan: form.nguoi_nhan || null,
      ly_do: form.ly_do || null,
      ghi_chu: form.ghi_chu || null,
      chi_tiet: form.chi_tiet.map((r) => ({
        san_pham: r.san_pham,
        so_luong: Number(r.so_luong),
      })),
    }
    await api.post(EP_PHIEU_XUAT, payload)
    showToast('Tạo phiếu xuất thành công')
    closeFormModal()
    await Promise.all([loadList(), loadSanPham()])
  } catch (e) {
    const d = e.response?.data
    formError.value =
      d?.error?.[0] ||
      d?.detail ||
      (typeof d === 'object' && d
        ? Object.entries(d).map(([k, v]) => `${k}: ${v}`).join('; ')
        : 'Có lỗi xảy ra, vui lòng thử lại')
  } finally {
    submitting.value = false
  }
}

function openDetail(item) {
  detailItem.value = item
  showDetailModal.value = true
}

// ===== In phiếu =====
function printPhieu(item) {
  if (!item) return

  const chiTietRows = (item.chi_tiet || []).map((ct, i) => `
    <tr>
      <td style="text-align:center">${i + 1}</td>
      <td>${ct.ten_sp || ''}</td>
      <td style="text-align:center">${ct.so_luong || 0}</td>
    </tr>
  `).join('')

  const tongSL = (item.chi_tiet || []).reduce(
    (s, ct) => s + (Number(ct.so_luong) || 0), 0
  )

  const html = `
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Phiếu xuất ${item.so_phieu || ''}</title>
<style>
  * { box-sizing: border-box; }
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 14px;
    color: #000;
    padding: 20px 30px;
    max-width: 800px;
    margin: 0 auto;
  }
  h2 { text-align: center; margin: 0 0 5px 0; font-size: 20px; }
  .subtitle { text-align: center; margin-bottom: 20px; font-style: italic; font-size: 13px; }
  .header-info { margin-bottom: 15px; }
  .header-info p { margin: 4px 0; }
  .header-info strong { display: inline-block; min-width: 130px; }
  table { width: 100%; border-collapse: collapse; margin: 15px 0; }
  th, td { border: 1px solid #000; padding: 6px 8px; }
  th { background: #f0f0f0; font-weight: bold; text-align: center; }
  tfoot td { font-weight: bold; }
  .signatures {
    display: flex;
    justify-content: space-between;
    margin-top: 40px;
    text-align: center;
  }
  .signatures div { width: 45%; }
  .signatures .title { font-weight: bold; margin-bottom: 80px; }
  .signatures .hint { font-style: italic; font-size: 12px; }
  @media print {
    body { padding: 0; }
    @page { margin: 15mm; }
  }
</style>
</head>
<body>
  <h2>PHIẾU XUẤT KHO</h2>
  <p class="subtitle">Số phiếu: ${item.so_phieu || '—'}</p>

  <div class="header-info">
    <p><strong>Ngày xuất:</strong> ${formatDate(item.ngay_xuat)}</p>
    <p><strong>Khoa phòng nhận:</strong> ${item.ten_kp || '—'}</p>
    <p><strong>Người nhận:</strong> ${item.nguoi_nhan || '—'}</p>
    <p><strong>Người lập:</strong> ${item.ten_nguoi_lap || '—'}</p>
    <p><strong>Lý do xuất:</strong> ${item.ly_do || '—'}</p>
    ${item.ghi_chu ? `<p><strong>Ghi chú:</strong> ${item.ghi_chu}</p>` : ''}
  </div>

  <table>
    <thead>
      <tr>
        <th style="width:50px">STT</th>
        <th>Tên sản phẩm</th>
        <th style="width:100px">Số lượng</th>
      </tr>
    </thead>
    <tbody>
      ${chiTietRows || '<tr><td colspan="3" style="text-align:center">Không có mặt hàng</td></tr>'}
    </tbody>
    <tfoot>
      <tr>
        <td colspan="2" style="text-align:right">Tổng cộng:</td>
        <td style="text-align:center">${tongSL}</td>
      </tr>
    </tfoot>
  </table>

  <div class="signatures">
    <div>
      <p class="title">Người lập phiếu</p>
      <p class="hint">(Ký, họ tên)</p>
    </div>
    <div>
      <p class="title">Người nhận hàng</p>
      <p class="hint">(Ký, họ tên)</p>
    </div>
  </div>

  <script>
    window.onload = function () {
      window.print();
    };
  <\/script>
</body>
</html>
  `

  const w = window.open('', '_blank', 'width=900,height=700')
  if (!w) {
    showToast('Trình duyệt chặn popup — vui lòng cho phép popup để in', 'error')
    return
  }
  w.document.open()
  w.document.write(html)
  w.document.close()
}

onMounted(async () => {
  await Promise.all([loadKhoaPhong(), loadSanPham(), loadList()])
})
</script>