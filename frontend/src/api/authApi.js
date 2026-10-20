import api from "./axios"

export const authApi = {
  async login({ username, password }) {
    const { data } = await api.post("/auth/login/", {
      ten_dang_nhap: username,
      mat_khau: password
    })
    return data
  },
  async me() {
    const { data } = await api.get("/auth/me/")
    return data
  },
  async logout(refresh) {
    await api.post("/auth/logout/", { refresh })
  }
}