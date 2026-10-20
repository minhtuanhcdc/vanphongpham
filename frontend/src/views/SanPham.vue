<template>
  <div class="space-y-5">
    <!-- Tiêu đề + nút thêm -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Sản phẩm</h1>
        <p class="text-sm text-gray-500 mt-1">
          Quản lý danh sách văn phòng phẩm trong kho
        </p>
      </div>
      <button
        @click="openCreate"
        class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
               hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="w-4 h-4" /> Thêm sản phẩm
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
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div class="relative sm:col-span-2">
          <MagnifyingGlassIcon
            class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2"
          />
          <input
            v-model="search"
            type="text"
            placeholder="Tìm theo tên hoặc mã sản phẩm..."
            class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm
                   outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>
        <select
          v-model="filterDanhMuc"
          class="px-3 py-2 border border-gray-300 rounded-lg text-sm outline-none
                 focus:border-blue-500"
        >
          <option value="">Tất cả danh mục</option>
          <option v-for="dm in danhMucList" :key="dm.ma_dm" :value="dm.ma_dm">
            {{ dm.ten_dm }}
          </option>
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
        <p class="text-4xl mb-2">📭</p>
        Không có sản phẩm nào
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr class="text-left text-gray-600">
              <th class="px-4 py-3 font-medium w-20">Mã</th>
              <th class="px-4 py-3 font-medium">Tên sản phẩm</th>
              <th class="px-4 py-3 font-medium">Danh mục</th>
              <th class="px-4 py-3 font-medium">Đơn vị</th>
              <th class="px-4 py-3 font-medium text-center">SL nhập</th>
              <th class="px-4 py-3 font-medium text-center">SL xuất</th>
              <th class="px-4 py-3 font-medium text-center">Tồn kho</th>
              <th class="px-4 py-3 font-medium text-center">Trạng thái tồn</th>
              <th class="px-4 py-3 font-medium text-right w-28">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedList"
              :key="item.ma_sp"
              class="border-b border-gray-50 hover:bg-gray-50 transition-colors"
            >
              <td class="px-4 py-3 font-mono text-xs text-gray-500">
                {{ item.ma_sp }}
              </td>
              <td class="px-4 py-3">
                <p class="font-medium text-gray-800">{{ item.ten_sp }}</p>
                <p v-if="item.han_su_dung" class="text-xs text-gray-400 mt-0.5">
                  HSD: {{ formatDate(item.han_su_dung) }}
                </p>
              </td>
              <td class="px-4 py-3 text-gray-600">
                {{ item.ten_dm || '—' }}
              </td>
              <td class="px-4 py-3 text-gray-600">
                {{ item.don_vi_tinh || '—' }}
              </td>
              <td class="px-4 py-3 text-center">
                <span class="text-xs font-semibold px-2 py-1 rounded-full bg-sky-100 text-sky-700">
                  {{ item.tong_nhap ?? 0 }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span class="text-xs font-semibold px-2 py-1 rounded-full bg-orange-100 text-orange-700">
                  {{ item.tong_xuat ?? 0 }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full whitespace-nowrap"
                  :class="tonKhoClass(item)"
                >
                  {{ item.so_luong_ton ?? 0 }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full whitespace-nowrap"
                  :class="tonKhoClass(item)"
                >
                  {{ item.so_luong_ton ?? 0 }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full"
                  :class="trangThaiTonClass(item.trang_thai_ton)"
                >
                  {{ labelTrangThaiTon(item.trang_thai_ton) }}
                </span>
              </td>
              <td class="px-4 py-3 text-right whitespace-nowrap">
                <button
                  @click="openEdit(item)"
                  class="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                  title="Sửa"
                >
                  <PencilIcon class="w-4 h-4" />
                </button>
                <button
                  @click="openDelete(item)"
                  class="p-1.5 text-red-600 hover:bg-red-50 rounded-lg transition ml-1"
                  title="Xoá"
                >
                  <TrashIcon class="w-4 h-4" />
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

    <!-- ===== MODAL THÊM / SỬA ===== -->
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
          <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-800">
                {{ isEditing ? 'Sửa sản phẩm' : 'Thêm sản phẩm' }}
              </h3>
              <button
                @click="closeFormModal"
                class="p-1.5 text-gray-400 hover:bg-gray-100 rounded-lg"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
              <!-- Tên sản phẩm -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Tên sản phẩm <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.ten_sp"
                  type="text"
                  placeholder="VD: Bút bi Thiên Long TL-027"
                  class="w-full px-3 py-2 border rounded-lg text-sm outline-none
                         focus:ring-1 focus:ring-blue-500"
                  :class="errors.ten_sp ? 'border-red-400' : 'border-gray-300 focus:border-blue-500'"
                />
                <p v-if="errors.ten_sp" class="text-xs text-red-600 mt-1">
                  {{ errors.ten_sp }}
                </p>
              </div>

              <!-- Danh mục -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Danh mục <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="form.danh_muc"
                  class="w-full px-3 py-2 border rounded-lg text-sm outline-none
                         focus:ring-1 focus:ring-blue-500"
                  :class="errors.danh_muc ? 'border-red-400' : 'border-gray-300 focus:border-blue-500'"
                >
                  <option :value="null">-- Chọn danh mục --</option>
                  <option v-for="dm in danhMucList" :key="dm.ma_dm" :value="dm.ma_dm">
                    {{ dm.ten_dm }}
                  </option>
                </select>
                <p v-if="errors.danh_muc" class="text-xs text-red-600 mt-1">
                  {{ errors.danh_muc }}
                </p>
              </div>

              <!-- Đơn vị tính + hạn sử dụng -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Đơn vị tính
                  </label>
                  <input
                    v-model="form.don_vi_tinh"
                    type="text"
                    placeholder="VD: cái, hộp, ram, quyển..."
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Hạn sử dụng
                  </label>
                  <input
                    v-model="form.han_su_dung"
                    type="date"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>

              <!-- Mức tồn tối thiểu + tối đa -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Mức tồn tối thiểu (cảnh báo sắp hết)
                  </label>
                  <input
                    v-model.number="form.muc_ton_toi_thieu"
                    type="number"
                    min="0"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Mức tồn tối đa (cảnh báo tồn cao)
                  </label>
                  <input
                    v-model.number="form.muc_ton_toi_da"
                    type="number"
                    min="0"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>

              <!-- Trạng thái -->
              <label class="flex items-center gap-2 cursor-pointer">
                <input v-model="form.trang_thai" type="checkbox" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Đang kinh doanh</span>
              </label>

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
                  :disabled="submitting"
                  class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
                         hover:bg-blue-700 transition disabled:opacity-60"
                >
                  {{ submitting ? 'Đang lưu...' : (isEditing ? 'Cập nhật' : 'Thêm') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- ===== MODAL XOÁ ===== -->
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
          v-if="showDeleteModal"
          class="fixed inset-0 z-40 bg-black/40 flex items-center justify-center p-4"
          @click.self="showDeleteModal = false"
        >
          <div class="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
            <div class="flex items-start gap-3">
              <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shrink-0">
                <ExclamationTriangleIcon class="w-5 h-5 text-red-600" />
              </div>
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-800">Xác nhận xoá</h3>
                <p class="text-sm text-gray-600 mt-1">
                  Bạn có chắc muốn xoá sản phẩm
                  <strong class="text-gray-800">{{ deletingItem?.ten_sp }}</strong>?
                  Hành động này không thể hoàn tác.
                </p>
              </div>
            </div>

            <p
              v-if="deleteError"
              class="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg mt-4"
            >
              {{ deleteError }}
            </p>

            <div class="flex justify-end gap-2 mt-6">
              <button
                @click="showDeleteModal = false"
                class="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Huỷ
              </button>
              <button
                @click="handleDelete"
                :disabled="deleting"
                class="px-4 py-2 text-sm bg-red-600 text-white rounded-lg
                       hover:bg-red-700 transition disabled:opacity-60"
              >
                {{ deleting ? 'Đang xoá...' : 'Xoá' }}
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
import api from '../api/axios'
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/24/outline'

// ===== Endpoints =====
const ENDPOINT   = '/products/san-pham/'
const EP_DANHMUC = '/products/danh-muc/'

// ===== State =====
const list = ref([])
const danhMucList = ref([])

const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)

const search = ref('')
const filterDanhMuc = ref('')
const page = ref(1)
const pageSize = 10

const showFormModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const deletingItem = ref(null)
const formError = ref('')
const deleteError = ref('')

const toast = reactive({ show: false, message: '', type: 'success' })
let toastTimer = null

const form = reactive({
  ten_sp: '',
  danh_muc: null,
  don_vi_tinh: 'cái',
  han_su_dung: '',
  muc_ton_toi_thieu: 5,
  muc_ton_toi_da: 1000,
  trang_thai: true,
})

const errors = reactive({ ten_sp: '', danh_muc: '' })

// ===== Computed =====
const filteredList = computed(() => {
  const kw = search.value.trim().toLowerCase()
  return list.value.filter((it) => {
    if (filterDanhMuc.value !== '' && it.danh_muc !== filterDanhMuc.value) return false
    if (!kw) return true
    return [it.ten_sp, it.ma_sp]
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

watch([search, filterDanhMuc], () => { page.value = 1 })
watch(totalPages, (tp) => { if (page.value > tp) page.value = tp })

// ===== Helpers =====
function formatDate(d) {
  if (!d) return '—'
  const dt = new Date(d)
  return dt.toLocaleDateString('vi-VN')
}

function tonKhoClass(item) {
  const ton = Number(item.so_luong_ton) || 0
  const min = Number(item.muc_ton_toi_thieu) || 0
  if (ton === 0) return 'bg-red-100 text-red-700'
  if (ton <= min) return 'bg-amber-100 text-amber-700'
  return 'bg-green-100 text-green-700'
}

function trangThaiTonClass(tt) {
  switch (tt) {
    case 'HET_HANG': return 'bg-red-100 text-red-700'
    case 'SAP_HET':  return 'bg-amber-100 text-amber-700'
    case 'TON_CAO':  return 'bg-blue-100 text-blue-700'
    default:         return 'bg-green-100 text-green-700'
  }
}

function labelTrangThaiTon(tt) {
  switch (tt) {
    case 'HET_HANG': return 'Hết hàng'
    case 'SAP_HET':  return 'Sắp hết'
    case 'TON_CAO':  return 'Tồn cao'
    default:         return 'Bình thường'
  }
}

function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toast.show = false), 2500)
}

function resetForm() {
  Object.assign(form, {
    ten_sp: '',
    danh_muc: null,
    don_vi_tinh: 'cái',
    han_su_dung: '',
    muc_ton_toi_thieu: 5,
    muc_ton_toi_da: 1000,
    trang_thai: true,
  })
  Object.keys(errors).forEach((k) => (errors[k] = ''))
  formError.value = ''
}

function validateForm() {
  errors.ten_sp = form.ten_sp.trim() ? '' : 'Vui lòng nhập tên sản phẩm'
  errors.danh_muc = form.danh_muc ? '' : 'Vui lòng chọn danh mục'
  return !errors.ten_sp && !errors.danh_muc
}

// ===== API =====
async function loadList() {
  loading.value = true
  try {
    const { data } = await api.get(ENDPOINT)
    list.value = data?.results ?? data ?? []
  } catch (e) {
    console.error('loadList:', e.response?.status, e.response?.data)
    showToast('Không tải được danh sách sản phẩm', 'error')
    list.value = []
  } finally {
    loading.value = false
  }
}

async function loadDanhMuc() {
  try {
    const { data } = await api.get(EP_DANHMUC)
    danhMucList.value = data?.results ?? data ?? []
  } catch {
    danhMucList.value = []
  }
}

function openCreate() {
  isEditing.value = false
  editingId.value = null
  resetForm()
  showFormModal.value = true
}

function openEdit(item) {
  isEditing.value = true
  editingId.value = item.ma_sp ?? item.id
  resetForm()
  Object.assign(form, {
    ten_sp: item.ten_sp ?? '',
    danh_muc: item.danh_muc ?? null,
    don_vi_tinh: item.don_vi_tinh ?? 'cái',
    han_su_dung: item.han_su_dung ?? '',
    muc_ton_toi_thieu: Number(item.muc_ton_toi_thieu) || 5,
    muc_ton_toi_da: Number(item.muc_ton_toi_da) || 1000,
    trang_thai: item.trang_thai ?? true,
  })
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  formError.value = ''
}

async function handleSubmit() {
  if (!validateForm()) return
  submitting.value = true
  formError.value = ''
  try {
    const payload = { ...form }
    // han_su_dung rỗng thì gửi null
    if (!payload.han_su_dung) payload.han_su_dung = null
    if (isEditing.value) {
      await api.put(`${ENDPOINT}${editingId.value}/`, payload)
      showToast('Cập nhật thành công')
    } else {
      await api.post(ENDPOINT, payload)
      showToast('Thêm mới thành công')
    }
    closeFormModal()
    await loadList()
  } catch (e) {
    const d = e.response?.data
    formError.value =
      d?.detail ||
      (typeof d === 'object' && d
        ? Object.entries(d).map(([k, v]) => `${k}: ${v}`).join('; ')
        : 'Có lỗi xảy ra, vui lòng thử lại')
  } finally {
    submitting.value = false
  }
}

function openDelete(item) {
  deletingItem.value = item
  deleteError.value = ''
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deletingItem.value) return
  deleting.value = true
  deleteError.value = ''
  try {
    const id = deletingItem.value.ma_sp ?? deletingItem.value.id
    await api.delete(`${ENDPOINT}${id}/`)
    showToast('Đã xoá sản phẩm')
    showDeleteModal.value = false
    await loadList()
  } catch (e) {
    deleteError.value =
      e.response?.data?.detail ||
      'Không thể xoá. Sản phẩm có thể đang được dùng trong phiếu nhập/xuất.'
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadDanhMuc(), loadList()])
})
</script>