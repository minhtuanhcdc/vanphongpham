<template>
  <div class="space-y-5">
    <!-- Tiêu đề + nút thêm -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Danh mục</h1>
        <p class="text-sm text-gray-500 mt-1">
          Quản lý danh mục văn phòng phẩm
        </p>
      </div>
      <button
        @click="openCreate"
        class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
               hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="w-4 h-4" /> Thêm danh mục
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
      <div class="relative">
        <MagnifyingGlassIcon
          class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2"
        />
        <input
          v-model="search"
          type="text"
          placeholder="Tìm theo tên hoặc mã danh mục..."
          class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm
                 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        />
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
        Không có danh mục nào
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr class="text-left text-gray-600">
              <th class="px-4 py-3 font-medium w-20">Mã</th>
              <th class="px-4 py-3 font-medium">Tên danh mục</th>
              <th class="px-4 py-3 font-medium">Mô tả</th>
              <th class="px-4 py-3 font-medium text-center w-32">Số sản phẩm</th>
              <th class="px-4 py-3 font-medium text-right w-28">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedList"
              :key="item.ma_dm"
              class="border-b border-gray-50 hover:bg-gray-50 transition-colors"
            >
              <td class="px-4 py-3 font-mono text-xs text-gray-500">
                {{ item.ma_dm }}
              </td>
              <td class="px-4 py-3 font-medium text-gray-800">
                {{ item.ten_dm }}
              </td>
              <td class="px-4 py-3 text-gray-600 max-w-md truncate" :title="item.mo_ta">
                {{ item.mo_ta || '—' }}
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full"
                  :class="item.so_san_pham > 0
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 text-gray-500'"
                >
                  {{ item.so_san_pham ?? 0 }}
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
          <div class="bg-white rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-800">
                {{ isEditing ? 'Sửa danh mục' : 'Thêm danh mục' }}
              </h3>
              <button
                @click="closeFormModal"
                class="p-1.5 text-gray-400 hover:bg-gray-100 rounded-lg"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Tên danh mục <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.ten_dm"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg text-sm outline-none
                         focus:ring-1 focus:ring-blue-500"
                  :class="errors.ten_dm ? 'border-red-400' : 'border-gray-300 focus:border-blue-500'"
                />
                <p v-if="errors.ten_dm" class="text-xs text-red-600 mt-1">
                  {{ errors.ten_dm }}
                </p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Mô tả
                </label>
                <textarea
                  v-model="form.mo_ta"
                  rows="4"
                  placeholder="Mô tả ngắn về danh mục này..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                         outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                ></textarea>
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
                  Bạn có chắc muốn xoá danh mục
                  <strong class="text-gray-800">{{ deletingItem?.ten_dm }}</strong>?
                  Hành động này không thể hoàn tác.
                </p>
                <p
                  v-if="deletingItem?.so_san_pham > 0"
                  class="text-sm text-amber-700 bg-amber-50 px-3 py-2 rounded-lg mt-3"
                >
                  ⚠️ Danh mục này đang có {{ deletingItem.so_san_pham }} sản phẩm.
                  Có thể không xoá được nếu backend chặn.
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

// Backend: apps/products/urls.py router.register('danh-muc', ...)
// → URL thật
const ENDPOINT = '/products/danh-muc/'

// ===== State =====
const list = ref([])
const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)

const search = ref('')
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
  ten_dm: '',
  mo_ta: '',
})

const errors = reactive({ ten_dm: '' })

// ===== Computed =====
const filteredList = computed(() => {
  const kw = search.value.trim().toLowerCase()
  if (!kw) return list.value
  return list.value.filter((it) =>
    [it.ten_dm, it.ma_dm, it.mo_ta]
      .filter(Boolean)
      .some((v) => String(v).toLowerCase().includes(kw))
  )
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredList.value.length / pageSize))
)

const paginatedList = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredList.value.slice(start, start + pageSize)
})

watch(search, () => { page.value = 1 })
watch(totalPages, (tp) => { if (page.value > tp) page.value = tp })

// ===== Helpers =====
function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toast.show = false), 2500)
}

function resetForm() {
  form.ten_dm = ''
  form.mo_ta = ''
  errors.ten_dm = ''
  formError.value = ''
}

function validateForm() {
  errors.ten_dm = form.ten_dm.trim() ? '' : 'Vui lòng nhập tên danh mục'
  return !errors.ten_dm
}

// ===== API =====
async function loadList() {
  loading.value = true
  try {
    const { data } = await api.get(ENDPOINT)
    list.value = data?.results ?? data ?? []
  } catch (e) {
    console.error('loadList error:', e.response?.status, e.response?.data)
    showToast('Không tải được danh sách danh mục', 'error')
    list.value = []
  } finally {
    loading.value = false
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
  editingId.value = item.ma_dm ?? item.id
  resetForm()
  form.ten_dm = item.ten_dm ?? ''
  form.mo_ta = item.mo_ta ?? ''
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
    const id = deletingItem.value.ma_dm ?? deletingItem.value.id
    await api.delete(`${ENDPOINT}${id}/`)
    showToast('Đã xoá danh mục')
    showDeleteModal.value = false
    await loadList()
  } catch (e) {
    deleteError.value =
      e.response?.data?.detail ||
      'Không thể xoá. Danh mục có thể đang được dùng bởi sản phẩm.'
  } finally {
    deleting.value = false
  }
}

onMounted(loadList)
</script>