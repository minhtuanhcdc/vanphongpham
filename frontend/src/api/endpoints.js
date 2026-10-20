
// src/api/endpoints.js
export const EP = {
  // Auth
  login:        '/auth/login/',
  refresh:      '/token/refresh/',      
  me:           '/auth/me/',

  // Products
  sanPham:      '/products/',           
  danhMuc:      '/products/categories/',
  nhaCungCap:   '/products/suppliers/', 

  // Inventory
  phieuNhap:    '/inventory/imports/',  
  phieuXuat:    '/inventory/exports/',  

  // Alerts
  canhBao:      '/alerts/',             
  canhBaoChuaXuLy: '/alerts/chua_xu_ly/', 
}