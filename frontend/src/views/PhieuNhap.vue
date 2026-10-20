<template>
  <div class="space-y-5">
    <!-- Tiêu đề + nút thêm -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Phiếu nhập kho</h1>
        <p class="text-sm text-gray-500 mt-1">
          Quản lý phiếu nhập văn phòng phẩm từ nhà cung cấp
        </p>
      </div>
      <button
        @click="openCreate"
        class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
               hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="w-4 h-4" /> Lập phiếu nhập
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
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="relative sm:col-span-2">
          <MagnifyingGlassIcon
            class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2"
          />
          <input
            v-model="search"
            type="text"
            placeholder="Tìm theo số phiếu, số hóa đơn, nhà cung cấp..."
            class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm
                   outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>
        <select
          v-model="filterTrangThai"
          class="px-3 py-2 border border-gray-300 rounded-lg text-sm
                 outline-none focus:border-blue-500"
        >
          <option value="">Tất cả trạng thái</option>
          <option value="NHAP">Đã nhập</option>
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
        <p class="text-4xl mb-2">📋</p>
        Chưa có phiếu nhập nào
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr class="text-left text-gray-600">
              <th class="px-4 py-3 font-medium w-16">Mã</th>
              <th class="px-4 py-3 font-medium">Số phiếu</th>
              <th class="px-4 py-3 font-medium">Nhà cung cấp</th>
              <th class="px-4 py-3 font-medium">Số hóa đơn</th>
              <th class="px-4 py-3 font-medium">Ngày nhập</th>
              <th class="px-4 py-3 font-medium text-center">Số mặt hàng</th>
              <th class="px-4 py-3 font-medium text-center">Trạng thái</th>
              <th class="px-4 py-3 font-medium text-right w-32">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedList"
              :key="item.ma_pn"
              class="border-b border-gray-50 hover:bg-gray-50 transition-colors"
            >
              <td class="px-4 py-3 font-mono text-xs text-gray-500">
                {{ item.ma_pn }}
              </td>
              <td class="px-4 py-3 font-medium text-gray-800">
                {{ item.so_phieu }}
              </td>
              <td class="px-4 py-3 text-gray-700">
                {{ item.ten_ncc || '—' }}
              </td>
              <td class="px-4 py-3 text-gray-600">
                {{ item.so_hoa_don || '—' }}
              </td>
              <td class="px-4 py-3 text-gray-600">
                {{ formatDate(item.ngay_nhap) }}
              </td>
              <td class="px-4 py-3 text-center">
                <span class="text-xs font-semibold px-2 py-1 rounded-full bg-blue-100 text-blue-700">
                  {{ item.chi_tiet?.length ?? 0 }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full"
                  :class="item.trang_thai === 'NHAP'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-500'"
                >
                  {{ item.trang_thai === 'NHAP' ? 'Đã nhập' : 'Đã hủy' }}
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
                <button
                  v-if="item.trang_thai === 'NHAP'"
                  @click="openCancel(item)"
                  class="p-1.5 text-red-600 hover:bg-red-50 rounded-lg transition ml-1"
                  title="Hủy phiếu"
                >
                  <XCircleIcon class="w-4 h-4" />
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

    <!-- ===== MODAL TẠO PHIẾU NHẬP ===== -->
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
              <h3 class="text-lg font-semibold text-gray-800">Lập phiếu nhập kho</h3>
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
                    placeholder="VD: PN-2026-001"
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
                    Nhà cung cấp
                  </label>
                  <select
                    v-model="form.nha_cung_cap"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  >
                    <option :value="null">-- Không chọn --</option>
                    <option v-for="ncc in nhaCungCapList" :key="ncc.ma_ncc" :value="ncc.ma_ncc">
                      {{ ncc.ten_ncc }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Số hóa đơn
                  </label>
                  <input
                    v-model="form.so_hoa_don"
                    type="text"
                    placeholder="VD: HD-12345"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm
                           outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
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
              </div>

              <!-- Chi tiết phiếu -->
              <div class="border-t border-gray-200 pt-4">
                <div class="flex items-center justify-between mb-3">
                  <h4 class="text-sm font-semibold text-gray-700">
                    Chi tiết mặt hàng <span class="text-red-500">*</span>
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
                    class="grid grid-cols-12 gap-2 items-start
                           bg-gray-50 rounded-lg p-3"
                  >
                    <div class="col-span-12 sm:col-span-4">
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
                          {{ sp.ten_sp }} ({{ sp.don_vi_tinh || '—' }})
                        </option>
                      </select>
                      <p v-if="rowErrors[idx]?.san_pham" class="text-xs text-red-600 mt-1">
                        {{ rowErrors[idx].san_pham }}
                      </p>
                    </div>
                    <div class="col-span-4 sm:col-span-2">
                      <label class="block text-xs text-gray-500 mb-1">Số lượng</label>
                      <input
                        v-model.number="row.so_luong"
                        type="number"
                        min="1"
                        class="w-full px-2 py-1.5 border rounded text-sm
                               outline-none focus:border-blue-500"
                        :class="rowErrors[idx]?.so_luong ? 'border-red-400' : 'border-gray-300'"
                      />
                    </div>
                    <div class="col-span-4 sm:col-span-2">
                      <label class="block text-xs text-gray-500 mb-1">Đơn giá (đ)</label>
                      <input
                        v-model.number="row.don_gia_nhap"
                        type="number"
                        min="0"
                        step="1000"
                        class="w-full px-2 py-1.5 border border-gray-300 rounded text-sm
                               outline-none focus:border-blue-500"
                      />
                    </div>
                    <div class="col-span-4 sm:col-span-3">
                      <label class="block text-xs text-gray-500 mb-1">Hạn sử dụng</label>
                      <input
                        v-model="row.han_su_dung"
                        type="date"
                        class="w-full px-2 py-1.5 border border-gray-300 rounded text-sm
                               outline-none focus:border-blue-500"
                      />
                    </div>
                    <div class="col-span-12 sm:col-span-1 flex justify-end">
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
                  <span class="text-gray-600">Tổng số lượng:</span>
                  <span class="font-semibold">{{ tongSoLuong }}</span>
                </div>
                <div class="flex justify-between mt-1">
                  <span class="text-gray-600">Tổng giá trị nhập:</span>
                  <span class="font-semibold text-blue-700">{{ formatMoney(tongGiaTri) }}</span>
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
                  :disabled="submitting"
                  class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg
                         hover:bg-blue-700 transition disabled:opacity-60"
                >
                  {{ submitting ? 'Đang lưu...' : 'Lưu phiếu nhập' }}
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
              <!-- Thông tin chung -->
              <div class="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <span class="text-gray-500">Số phiếu:</span>
                  <span class="font-medium ml-2">{{ detailItem.so_phieu }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Ngày nhập:</span>
                  <span class="font-medium ml-2">{{ formatDate(detailItem.ngay_nhap) }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Nhà cung cấp:</span>
                  <span class="font-medium ml-2">{{ detailItem.ten_ncc || '—' }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Số hóa đơn:</span>
                  <span class="font-medium ml-2">{{ detailItem.so_hoa_don || '—' }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Người lập:</span>
                  <span class="font-medium ml-2">{{ detailItem.ten_nguoi_lap || '—' }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Trạng thái:</span>
                  <span
                    class="text-xs font-semibold px-2 py-0.5 rounded-full ml-2"
                    :class="detailItem.trang_thai === 'NHAP'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-500'"
                  >
                    {{ detailItem.trang_thai === 'NHAP' ? 'Đã nhập' : 'Đã hủy' }}
                  </span>
                </div>
              </div>

              <p v-if="detailItem.ghi_chu" class="text-sm text-gray-600 italic">
                Ghi chú: {{ detailItem.ghi_chu }}
              </p>

              <!-- Bảng chi tiết -->
              <div class="border border-gray-200 rounded-lg overflow-hidden">
                <table class="w-full text-sm">
                  <thead class="bg-gray-50 border-b border-gray-200">
                    <tr class="text-left text-gray-600">
                      <th class="px-3 py-2 font-medium">Sản phẩm</th>
                      <th class="px-3 py-2 font-medium text-right">Số lượng</th>
                      <th class="px-3 py-2 font-medium text-right">Đơn giá</th>
                      <th class="px-3 py-2 font-medium text-right">Thành tiền</th>
                      <th class="px-3 py-2 font-medium text-center">HSD</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="ct in detailItem.chi_tiet"
                      :key="ct.id"
                      class="border-b border-gray-100"
                    >
                      <td class="px-3 py-2">{{ ct.ten_sp }}</td>
                      <td class="px-3 py-2 text-right">{{ ct.so_luong }}</td>
                      <td class="px-3 py-2 text-right">
                        {{ formatMoney(ct.don_gia_nhap) }}
                      </td>
                      <td class="px-3 py-2 text-right font-medium">
                        {{ formatMoney((ct.so_luong || 0) * (ct.don_gia_nhap || 0)) }}
                      </td>
                      <td class="px-3 py-2 text-center text-gray-500">
                        {{ ct.han_su_dung ? formatDate(ct.han_su_dung) : '—' }}
                      </td>
                    </tr>
                  </tbody>
                  <tfoot class="bg-gray-50 border-t border-gray-200">
                    <tr>
                      <td colspan="3" class="px-3 py-2 text-right font-semibold">
                        Tổng cộng:
                      </td>
                      <td class="px-3 py-2 text-right font-bold text-blue-700">
                        {{ formatMoney(tongTienChiTiet(detailItem)) }}
                      </td>
                      <td></td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>

            <div class="px-6 py-4 border-t border-gray-200 flex justify-end">
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

    <!-- ===== MODAL HỦY PHIẾU ===== -->
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
          v-if="showCancelModal"
          class="fixed inset-0 z-40 bg-black/40 flex items-center justify-center p-4"
          @click.self="showCancelModal = false"
        >
          <div class="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
            <div class="flex items-start gap-3">
              <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shrink-0">
                <ExclamationTriangleIcon class="w-5 h-5 text-red-600" />
              </div>
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-800">Hủy phiếu nhập</h3>
                <p class="text-sm text-gray-600 mt-1">
                  Bạn có chắc muốn hủy phiếu
                  <strong class="text-gray-800">{{ cancelItem?.so_phieu }}</strong>?
                  Hành động này sẽ trừ lại số lượng đã nhập khỏi kho.
                </p>
              </div>
            </div>

            <p
              v-if="cancelError"
              class="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg mt-4"
            >
              {{ cancelError }}
            </p>

            <div class="flex justify-end gap-2 mt-6">
              <button
                @click="showCancelModal = false"
                class="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Không
              </button>
              <button
                @click="handleCancel"
                :disabled="cancelling"
                class="px-4 py-2 text-sm bg-red-600 text-white rounded-lg
                       hover:bg-red-700 transition disabled:opacity-60"
              >
                {{ cancelling ? 'Đang hủy...' : 'Hủy phiếu' }}
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
  XCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/24/outline'

// ===== Endpoints =====
const EP_PHIEU_NHAP = '/inventory/phieu-nhap/'
const EP_NCC        = '/products/nha-cung-cap/'
const EP_SAN_PHAM   = '/products/san-pham/'

// ===== State =====
const list = ref([])
const nhaCungCapList = ref([])
const sanPhamList = ref([])

const loading = ref(false)
const submitting = ref(false)
const cancelling = ref(false)

const search = ref('')
const filterTrangThai = ref('')
const page = ref(1)
const pageSize = 10

const showFormModal = ref(false)
const showDetailModal = ref(false)
const showCancelModal = ref(false)
const detailItem = ref(null)
const cancelItem = ref(null)
const formError = ref('')
const cancelError = ref('')

const toast = reactive({ show: false, message: '', type: 'success' })
let toastTimer = null

const form = reactive({
  so_phieu: '',
  nha_cung_cap: null,
  so_hoa_don: '',
  ghi_chu: '',
  chi_tiet: [],
})

const errors = reactive({ so_phieu: '' })
const rowErrors = ref([])

// ===== Computed =====
const filteredList = computed(() => {
  const kw = search.value.trim().toLowerCase()
  return list.value.filter((it) => {
    if (filterTrangThai.value && it.trang_thai !== filterTrangThai.value) return false
    if (!kw) return true
    return [it.so_phieu, it.so_hoa_don, it.ten_ncc]
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

const tongGiaTri = computed(() =>
  form.chi_tiet.reduce(
    (s, r) => s + (Number(r.so_luong) || 0) * (Number(r.don_gia_nhap) || 0),
    0
  )
)

watch([search, filterTrangThai], () => { page.value = 1 })
watch(totalPages, (tp) => { if (page.value > tp) page.value = tp })

// ===== Helpers =====
function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('vi-VN')
}

function formatMoney(n) {
  if (n === null || n === undefined || n === '') return '—'
  return Number(n).toLocaleString('vi-VN') + ' đ'
}

function tongTienChiTiet(item) {
  if (!item?.chi_tiet) return 0
  return item.chi_tiet.reduce(
    (s, ct) => s + (Number(ct.so_luong) || 0) * (Number(ct.don_gia_nhap) || 0),
    0
  )
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
    so_phieu: '',
    nha_cung_cap: null,
    so_hoa_don: '',
    ghi_chu: '',
    chi_tiet: [],
  })
  Object.keys(errors).forEach((k) => (errors[k] = ''))
  rowErrors.value = []
  formError.value = ''
}

function validateForm() {
  errors.so_phieu = form.so_phieu.trim() ? '' : 'Vui lòng nhập số phiếu'
  rowErrors.value = form.chi_tiet.map((r) => {
    const e = {}
    if (!r.san_pham) e.san_pham = 'Chọn sản phẩm'
    if (!r.so_luong || r.so_luong <= 0) e.so_luong = 'SL > 0'
    return e
  })
  const hasRowErr = rowErrors.value.some((e) => Object.keys(e).length > 0)
  if (form.chi_tiet.length === 0) {
    formError.value = 'Vui lòng thêm ít nhất 1 mặt hàng'
    return false
  }
  return !errors.so_phieu && !hasRowErr
}

// ===== API =====
async function loadList() {
  loading.value = true
  try {
    const { data } = await api.get(EP_PHIEU_NHAP)
    list.value = data?.results ?? data ?? []
  } catch (e) {
    console.error('loadList:', e.response?.status, e.response?.data)
    showToast('Không tải được danh sách phiếu nhập', 'error')
    list.value = []
  } finally {
    loading.value = false
  }
}

async function loadNhaCungCap() {
  try {
    const { data } = await api.get(EP_NCC)
    nhaCungCapList.value = data?.results ?? data ?? []
  } catch {
    nhaCungCapList.value = []
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
  // Sinh số phiếu tạm theo timestamp
  const now = new Date()
  const ymd = now.toISOString().slice(0, 10).replace(/-/g, '')
  const rand = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  form.so_phieu = `PN-${ymd}-${rand}`
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
    don_gia_nhap: 0,
    han_su_dung: '',
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
      nha_cung_cap: form.nha_cung_cap,
      so_hoa_don: form.so_hoa_don || null,
      ghi_chu: form.ghi_chu || null,
      chi_tiet: form.chi_tiet.map((r) => ({
        san_pham: r.san_pham,
        so_luong: Number(r.so_luong),
        don_gia_nhap: r.don_gia_nhap || null,
        han_su_dung: r.han_su_dung || null,
      })),
    }
    await api.post(EP_PHIEU_NHAP, payload)
    showToast('Tạo phiếu nhập thành công')
    closeFormModal()
    await loadList()
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

function openCancel(item) {
  cancelItem.value = item
  cancelError.value = ''
  showCancelModal.value = true
}

async function handleCancel() {
  if (!cancelItem.value) return
  cancelling.value = true
  cancelError.value = ''
  try {
    // Cập nhật trạng thái phiếu thành HUY
    await api.patch(`${EP_PHIEU_NHAP}${cancelItem.value.ma_pn}/`, {
      trang_thai: 'HUY',
    })
    showToast('Đã hủy phiếu nhập')
    showCancelModal.value = false
    await loadList()
  } catch (e) {
    cancelError.value =
      e.response?.data?.detail ||
      'Không thể hủy phiếu. Vui lòng thử lại.'
  } finally {
    cancelling.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadNhaCungCap(), loadSanPham(), loadList()])
})
</script>