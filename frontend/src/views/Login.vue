<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route  = useRoute()
const auth   = useAuthStore()

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const errors = reactive({ ten_dang_nhap: '', mat_khau: '' })
const alert  = reactive({ message: '', type: 'error' })
const showPassword = ref(false)
const isLoading    = ref(false)

/* Validation */
function validateUsername() {
  const v = form.username.trim()
  if (!v) { errors.ten_dang_nhap = 'Vui lòng nhập tên đăng nhập'; return false }
  if (v.length < 3) { errors.ten_dang_nhap = 'Tối thiểu 3 ký tự'; return false }
  errors.ten_dang_nhap = ''
  return true
}
function validatePassword() {
  const v = form.password
  if (!v) { errors.mat_khau = 'Vui lòng nhập mật khẩu'; return false }
  if (v.length < 3) { errors.mat_khau = 'Tối thiểu 3 ký tự'; return false }
  errors.mat_khau = ''
  return true
}

async function handleSubmit() {
  alert.message = ''

  if (!validateUsername() || !validatePassword()) {
    alert.message = 'Vui lòng kiểm tra lại thông tin'
    alert.type = 'error'
    return
  }

  isLoading.value = true
  try {
    await auth.login({
      username: form.username.trim(),
      password: form.password,
    })

    if (form.remember) localStorage.setItem('saved_username', form.username.trim())
    else               localStorage.removeItem('saved_username')

    alert.message = 'Đăng nhập thành công! Đang chuyển hướng...'
    alert.type = 'success'

    const redirect = route.query.redirect || '/dashboard'
    await new Promise(r => setTimeout(r, 300))   // tuỳ chọn: cho user kịp đọc
    await router.push(redirect)
  } catch (err) {
    // Nếu lỗi xảy ra trong router.push, err sẽ không có .response
    if (err?.response) {
      alert.message =
        err.response.data?.detail ||
        err.response.data?.non_field_errors?.[0] ||
        'Tên đăng nhập hoặc mật khẩu không đúng'
    } else {
      alert.message = 'Không thể chuyển trang, vui lòng thử lại'
      console.error('Navigation error:', err)
    }
    alert.type = 'error'
  } finally {
    isLoading.value = false
  }
}
onMounted(() => {
  const saved = localStorage.getItem('saved_username')
  if (saved) {
    form.username = saved
    form.remember = true
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 p-4">
    <form
      class="bg-white p-8 rounded-xl shadow-lg w-full max-w-sm"
      @submit.prevent="handleSubmit"
    >
      <h2 class="text-2xl font-bold text-center mb-5">Đăng nhập</h2>

      <p
        v-if="alert.message"
        class="px-3 py-2 rounded-lg text-sm mb-4"
        :class="alert.type === 'success'
          ? 'bg-green-50 text-green-700'
          : 'bg-red-50 text-red-700'"
      >
        {{ alert.message }}
      </p>

      <div class="flex flex-col mb-4">
        <label for="username" class="text-sm text-gray-700 mb-1.5">
          Tên đăng nhập
        </label>
        <input
          id="username"
          v-model="form.username"
          type="text"
          autocomplete="username"
          class="px-3 py-2.5 border border-slate-300 rounded-lg text-base outline-none
                 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
          @blur="validateUsername"
        />
        <small v-if="errors.ten_dang_nhap" class="text-red-600 text-xs mt-1">
          {{ errors.ten_dang_nhap }}
        </small>
      </div>

      <div class="flex flex-col mb-4">
        <label for="password" class="text-sm text-gray-700 mb-1.5">
          Mật khẩu
        </label>
        <div class="flex">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="current-password"
            class="flex-1 px-3 py-2.5 border border-slate-300 rounded-lg text-base outline-none
                   focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            @blur="validatePassword"
          />
          <button
            type="button"
            class="ml-2 px-3 border border-slate-300 bg-slate-100 rounded-lg cursor-pointer
                   text-sm hover:bg-slate-200 transition"
            @click="showPassword = !showPassword"
          >
            {{ showPassword ? 'Ẩn' : 'Hiện' }}
          </button>
        </div>
        <small v-if="errors.mat_khau" class="text-red-600 text-xs mt-1">
          {{ errors.mat_khau }}
        </small>
      </div>

      <label class="flex items-center gap-1.5 text-sm mb-4 cursor-pointer">
        <input v-model="form.remember" type="checkbox" />
        Ghi nhớ đăng nhập
      </label>

      <button
        type="submit"
        :disabled="isLoading"
        class="w-full py-2.5 bg-blue-500 text-white rounded-lg text-base cursor-pointer
               hover:bg-blue-600 transition
               disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {{ isLoading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
      </button>

      <p class="text-center mt-4 text-sm">
        Chưa có tài khoản?
        <RouterLink to="/register" class="text-blue-500 hover:underline">
          Đăng ký
        </RouterLink>
      </p>
    </form>
  </div>
</template>