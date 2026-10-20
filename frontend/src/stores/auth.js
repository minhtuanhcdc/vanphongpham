
import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { authApi } from "@/api/authApi"

export const useAuthStore = defineStore("auth", () => {
  const user         = ref(JSON.parse(localStorage.getItem("user") || "null"))
  const accessToken  = ref(localStorage.getItem("access_token") || "")
  const refreshToken = ref(localStorage.getItem("refresh_token") || "")
  const loading      = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin         = computed(() => user.value?.role === "admin")
  const fullName        = computed(
    () => user.value?.full_name || user.value?.username || ""
  )

  async function login(credentials) {
    loading.value = true
    try {
      const data = await authApi.login(credentials)
      _setSession(data)
      return data
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    if (!accessToken.value) return
    try {
      const me = await authApi.me()
      user.value = me
      localStorage.setItem("user", JSON.stringify(me))
    } catch {
      logout()
    }
  }

  async function logout() {
    try {
      if (refreshToken.value) await authApi.logout(refreshToken.value)
    } catch { /* ignore */ }
    _clearSession()
  }

  function _setSession(raw) {
  console.log('🔵 _setSession input:', raw)

  // Unwrap nếu response bọc trong `data`
  const d = raw?.data ?? raw

  // Tìm access token ở mọi key phổ biến
  const access =
    d?.access ??
    d?.access_token ??
    d?.token ??
    d?.jwt ??
    ''

  const refresh =
    d?.refresh ??
    d?.refresh_token ??
    ''

  // Tìm user ở mọi key phổ biến
  const u =
    d?.user ??
    d?.nguoi_dung ??
    d?.profile ??
    null

  console.log('🔵 parsed:', { access: !!access, refresh: !!refresh, user: u })

  if (!access) {
    throw new Error(
      'Login response thiếu access token. Response keys: ' +
      Object.keys(d || {}).join(', ')
    )
  }

  accessToken.value  = access
  refreshToken.value = refresh
  user.value         = u

  localStorage.setItem('access_token',  access)
  localStorage.setItem('refresh_token', refresh)
  if (u) localStorage.setItem('user', JSON.stringify(u))
}

  function _clearSession() {
    accessToken.value  = ""
    refreshToken.value = ""
    user.value         = null
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    localStorage.removeItem("user")
  }

  return {
    user, accessToken, refreshToken, loading,
    isAuthenticated, isAdmin, fullName,
    login, logout, fetchMe
  }
})
