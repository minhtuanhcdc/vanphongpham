import axios from "axios"

const api = axios.create({
  baseURL: "/api",
  timeout: 15000,
  headers: { "Content-Type": "application/json" }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token")
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let isRefreshing = false
let queue = []

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      const refresh = localStorage.getItem("refresh_token")
      if (!refresh) {
        localStorage.clear()
        window.location.href = "/login"
        return Promise.reject(error)
      }
      if (isRefreshing) {
        return new Promise((resolve) => {
          queue.push((token) => {
            original.headers.Authorization = `Bearer ${token}`
            resolve(api(original))
          })
        })
      }
      original._retry = true
      isRefreshing = true
      try {
        const { data } = await axios.post("/api/auth/refresh/", { refresh })  // 👈 đổi
        localStorage.setItem("access_token", data.access)
        queue.forEach((cb) => cb(data.access))
        queue = []
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)
      } catch (err) {
        localStorage.clear()
        window.location.href = "/login"
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  }
)

export default api