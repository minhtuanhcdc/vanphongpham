-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 20, 2026 at 08:25 AM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `quanlykho_vpp`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add tai khoan', 6, 'add_taikhoan'),
(22, 'Can change tai khoan', 6, 'change_taikhoan'),
(23, 'Can delete tai khoan', 6, 'delete_taikhoan'),
(24, 'Can view tai khoan', 6, 'view_taikhoan'),
(25, 'Can add danh muc', 7, 'add_danhmuc'),
(26, 'Can change danh muc', 7, 'change_danhmuc'),
(27, 'Can delete danh muc', 7, 'delete_danhmuc'),
(28, 'Can view danh muc', 7, 'view_danhmuc'),
(29, 'Can add nha cung cap', 8, 'add_nhacungcap'),
(30, 'Can change nha cung cap', 8, 'change_nhacungcap'),
(31, 'Can delete nha cung cap', 8, 'delete_nhacungcap'),
(32, 'Can view nha cung cap', 8, 'view_nhacungcap'),
(33, 'Can add san pham', 9, 'add_sanpham'),
(34, 'Can change san pham', 9, 'change_sanpham'),
(35, 'Can delete san pham', 9, 'delete_sanpham'),
(36, 'Can view san pham', 9, 'view_sanpham'),
(37, 'Can add phieu nhap', 10, 'add_phieunhap'),
(38, 'Can change phieu nhap', 10, 'change_phieunhap'),
(39, 'Can delete phieu nhap', 10, 'delete_phieunhap'),
(40, 'Can view phieu nhap', 10, 'view_phieunhap'),
(41, 'Can add phieu xuat', 11, 'add_phieuxuat'),
(42, 'Can change phieu xuat', 11, 'change_phieuxuat'),
(43, 'Can delete phieu xuat', 11, 'delete_phieuxuat'),
(44, 'Can view phieu xuat', 11, 'view_phieuxuat'),
(45, 'Can add chi tiet phieu nhap', 12, 'add_chitietphieunhap'),
(46, 'Can change chi tiet phieu nhap', 12, 'change_chitietphieunhap'),
(47, 'Can delete chi tiet phieu nhap', 12, 'delete_chitietphieunhap'),
(48, 'Can view chi tiet phieu nhap', 12, 'view_chitietphieunhap'),
(49, 'Can add chi tiet phieu xuat', 13, 'add_chitietphieuxuat'),
(50, 'Can change chi tiet phieu xuat', 13, 'change_chitietphieuxuat'),
(51, 'Can delete chi tiet phieu xuat', 13, 'delete_chitietphieuxuat'),
(52, 'Can view chi tiet phieu xuat', 13, 'view_chitietphieuxuat'),
(53, 'Can add canh bao', 14, 'add_canhbao'),
(54, 'Can change canh bao', 14, 'change_canhbao'),
(55, 'Can delete canh bao', 14, 'delete_canhbao'),
(56, 'Can view canh bao', 14, 'view_canhbao'),
(57, 'Can add khoa phong', 15, 'add_khoaphong'),
(58, 'Can change khoa phong', 15, 'change_khoaphong'),
(59, 'Can delete khoa phong', 15, 'delete_khoaphong'),
(60, 'Can view khoa phong', 15, 'view_khoaphong'),
(61, 'Can add lich su kho', 16, 'add_lichsukho'),
(62, 'Can change lich su kho', 16, 'change_lichsukho'),
(63, 'Can delete lich su kho', 16, 'delete_lichsukho'),
(64, 'Can view lich su kho', 16, 'view_lichsukho');

-- --------------------------------------------------------

--
-- Table structure for table `canh_bao`
--

DROP TABLE IF EXISTS `canh_bao`;
CREATE TABLE IF NOT EXISTS `canh_bao` (
  `ma_cb` int NOT NULL AUTO_INCREMENT,
  `loai_canh_bao` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `so_luong_ton` int NOT NULL,
  `noi_dung` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ngay_canh_bao` datetime(6) NOT NULL,
  `da_xu_ly` tinyint(1) NOT NULL,
  `ma_sp` int NOT NULL,
  PRIMARY KEY (`ma_cb`),
  KEY `canh_bao_ma_sp_2c4e9361` (`ma_sp`),
  KEY `canh_bao_ma_sp_8753bb_idx` (`ma_sp`,`da_xu_ly`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `chi_tiet_phieu_nhap`
--

DROP TABLE IF EXISTS `chi_tiet_phieu_nhap`;
CREATE TABLE IF NOT EXISTS `chi_tiet_phieu_nhap` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `so_luong` int NOT NULL,
  `ma_sp` int NOT NULL,
  `ma_pn` int NOT NULL,
  `don_gia_nhap` decimal(15,2) DEFAULT NULL,
  `han_su_dung` date DEFAULT NULL,
  `so_luong_con_lai` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chi_tiet_phieu_nhap_ma_sp_b4e84c49` (`ma_sp`),
  KEY `chi_tiet_phieu_nhap_ma_pn_62e8b512` (`ma_pn`)
) ;

--
-- Dumping data for table `chi_tiet_phieu_nhap`
--

INSERT INTO `chi_tiet_phieu_nhap` (`id`, `so_luong`, `ma_sp`, `ma_pn`, `don_gia_nhap`, `han_su_dung`, `so_luong_con_lai`) VALUES
(1, 100, 1, 1, 3000.00, '2027-10-18', 80),
(2, 100, 2, 2, 1000.00, NULL, 80),
(3, 100, 1, 2, 2000.00, NULL, 100);

-- --------------------------------------------------------

--
-- Table structure for table `chi_tiet_phieu_xuat`
--

DROP TABLE IF EXISTS `chi_tiet_phieu_xuat`;
CREATE TABLE IF NOT EXISTS `chi_tiet_phieu_xuat` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `so_luong` int NOT NULL,
  `ma_sp` int NOT NULL,
  `ma_px` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chi_tiet_phieu_xuat_ma_sp_dd0dea98` (`ma_sp`),
  KEY `chi_tiet_phieu_xuat_ma_px_989add93` (`ma_px`)
) ;

--
-- Dumping data for table `chi_tiet_phieu_xuat`
--

INSERT INTO `chi_tiet_phieu_xuat` (`id`, `so_luong`, `ma_sp`, `ma_px`) VALUES
(1, 10, 2, 1),
(2, 10, 2, 2),
(3, 20, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `danh_muc`
--

DROP TABLE IF EXISTS `danh_muc`;
CREATE TABLE IF NOT EXISTS `danh_muc` (
  `ma_dm` int NOT NULL AUTO_INCREMENT,
  `ten_dm` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mo_ta` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ma_dm`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `danh_muc`
--

INSERT INTO `danh_muc` (`ma_dm`, `ten_dm`, `mo_ta`) VALUES
(1, 'Bút bi', 'Các loại bút bi');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'accounts', 'taikhoan'),
(7, 'products', 'danhmuc'),
(8, 'products', 'nhacungcap'),
(9, 'products', 'sanpham'),
(10, 'inventory', 'phieunhap'),
(11, 'inventory', 'phieuxuat'),
(12, 'inventory', 'chitietphieunhap'),
(13, 'inventory', 'chitietphieuxuat'),
(14, 'alerts', 'canhbao'),
(15, 'departments', 'khoaphong'),
(16, 'inventory', 'lichsukho');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-10-09 14:41:52.907075'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-10-09 14:41:52.942289'),
(3, 'auth', '0001_initial', '2026-10-09 14:41:53.077884'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-10-09 14:41:53.097050'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-10-09 14:41:53.101049'),
(6, 'auth', '0004_alter_user_username_opts', '2026-10-09 14:41:53.105048'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-10-09 14:41:53.109048'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-10-09 14:41:53.110047'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-10-09 14:41:53.114053'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-10-09 14:41:53.119052'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-10-09 14:41:53.123081'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-10-09 14:41:53.142048'),
(13, 'auth', '0011_update_proxy_permissions', '2026-10-09 14:41:53.146064'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-10-09 14:41:53.150049'),
(15, 'accounts', '0001_initial', '2026-10-09 14:41:53.324377'),
(16, 'admin', '0001_initial', '2026-10-09 14:41:53.421431'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-10-09 14:41:53.427461'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-10-09 14:41:53.432430'),
(19, 'products', '0001_initial', '2026-10-09 14:41:53.516106'),
(20, 'alerts', '0001_initial', '2026-10-09 14:41:53.556878'),
(21, 'inventory', '0001_initial', '2026-10-09 14:41:53.854527'),
(22, 'sessions', '0001_initial', '2026-10-09 14:41:53.876935'),
(23, 'departments', '0001_initial', '2026-10-17 08:58:53.974607'),
(24, 'products', '0002_alter_danhmuc_options_alter_nhacungcap_options_and_more', '2026-10-18 03:21:02.555727'),
(25, 'alerts', '0002_alter_canhbao_san_pham_and_more', '2026-10-18 03:21:02.577886'),
(26, 'inventory', '0002_lichsukho_alter_chitietphieunhap_unique_together_and_more', '2026-10-18 03:21:03.465622');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `khoa_phong`
--

DROP TABLE IF EXISTS `khoa_phong`;
CREATE TABLE IF NOT EXISTS `khoa_phong` (
  `ma_kp` int NOT NULL AUTO_INCREMENT,
  `ten_kp` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mo_ta` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trang_thai` tinyint(1) NOT NULL,
  PRIMARY KEY (`ma_kp`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `khoa_phong`
--

INSERT INTO `khoa_phong` (`ma_kp`, `ten_kp`, `mo_ta`, `trang_thai`) VALUES
(1, 'Phòng Công Nghệ Thông Tin', '', 1),
(2, 'Phòng Tổ Chức Hành Chính', '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `lich_su_kho`
--

DROP TABLE IF EXISTS `lich_su_kho`;
CREATE TABLE IF NOT EXISTS `lich_su_kho` (
  `ma_lsk` int NOT NULL AUTO_INCREMENT,
  `loai` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `so_luong_thay_doi` int NOT NULL,
  `so_luong_sau` int NOT NULL,
  `tham_chieu` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `thoi_gian` datetime(6) NOT NULL,
  `ghi_chu` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ma_tk` int DEFAULT NULL,
  `ma_sp` int NOT NULL,
  PRIMARY KEY (`ma_lsk`),
  KEY `lich_su_kho_ma_sp_1769f1_idx` (`ma_sp`,`thoi_gian`),
  KEY `lich_su_kho_ma_tk_25bc4e69` (`ma_tk`),
  KEY `lich_su_kho_ma_sp_16ed3a49` (`ma_sp`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `lich_su_kho`
--

INSERT INTO `lich_su_kho` (`ma_lsk`, `loai`, `so_luong_thay_doi`, `so_luong_sau`, `tham_chieu`, `thoi_gian`, `ghi_chu`, `ma_tk`, `ma_sp`) VALUES
(1, 'NHAP', 100, 100, 'PN-20261018-431', '2026-10-18 03:43:27.388479', NULL, 1, 1),
(2, 'NHAP', 100, 100, 'PN-20261018-745', '2026-10-18 03:48:41.223013', NULL, 1, 2),
(3, 'NHAP', 100, 200, 'PN-20261018-745', '2026-10-18 03:48:41.225099', NULL, 1, 1),
(4, 'XUAT', -10, 90, 'PX-20261018-644', '2026-10-18 04:13:53.609093', NULL, 1, 2),
(5, 'XUAT', -10, 80, 'PX-20261018-079', '2026-10-18 15:05:37.156137', NULL, 1, 2),
(6, 'XUAT', -20, 180, 'PX-20261018-079', '2026-10-18 15:05:37.164680', NULL, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `nha_cung_cap`
--

DROP TABLE IF EXISTS `nha_cung_cap`;
CREATE TABLE IF NOT EXISTS `nha_cung_cap` (
  `ma_ncc` int NOT NULL AUTO_INCREMENT,
  `ten_ncc` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dia_chi` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dien_thoai` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trang_thai` tinyint(1) NOT NULL,
  PRIMARY KEY (`ma_ncc`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `nha_cung_cap`
--

INSERT INTO `nha_cung_cap` (`ma_ncc`, `ten_ncc`, `dia_chi`, `dien_thoai`, `email`, `trang_thai`) VALUES
(1, 'Công ty Văn phòng phẩm Hùng Hà', '246 Trần Hưng Đạo, P. Chợ Quán, Tp.HCM', NULL, '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `phieu_nhap`
--

DROP TABLE IF EXISTS `phieu_nhap`;
CREATE TABLE IF NOT EXISTS `phieu_nhap` (
  `ma_pn` int NOT NULL AUTO_INCREMENT,
  `ngay_nhap` datetime(6) NOT NULL,
  `ghi_chu` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ma_tk` int DEFAULT NULL,
  `ma_ncc` int DEFAULT NULL,
  `so_hoa_don` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `so_phieu` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `trang_thai` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`ma_pn`),
  UNIQUE KEY `so_phieu` (`so_phieu`),
  KEY `phieu_nhap_ma_tk_530caab7` (`ma_tk`),
  KEY `phieu_nhap_ma_ncc_489f9c11` (`ma_ncc`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `phieu_nhap`
--

INSERT INTO `phieu_nhap` (`ma_pn`, `ngay_nhap`, `ghi_chu`, `ma_tk`, `ma_ncc`, `so_hoa_don`, `so_phieu`, `trang_thai`) VALUES
(1, '2026-10-18 03:43:27.384477', NULL, 1, 1, 'HD00001', 'PN-20261018-431', 'NHAP'),
(2, '2026-10-18 03:48:41.220043', NULL, 1, 1, 'HD0002', 'PN-20261018-745', 'NHAP');

-- --------------------------------------------------------

--
-- Table structure for table `phieu_xuat`
--

DROP TABLE IF EXISTS `phieu_xuat`;
CREATE TABLE IF NOT EXISTS `phieu_xuat` (
  `ma_px` int NOT NULL AUTO_INCREMENT,
  `ngay_xuat` datetime(6) NOT NULL,
  `nguoi_nhan` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ly_do` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ma_tk` int DEFAULT NULL,
  `ghi_chu` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ma_kp` int NOT NULL,
  `so_phieu` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `trang_thai` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`ma_px`),
  UNIQUE KEY `so_phieu` (`so_phieu`),
  KEY `phieu_xuat_ma_tk_8875535a` (`ma_tk`),
  KEY `phieu_xuat_ma_kp_e95611ca` (`ma_kp`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `phieu_xuat`
--

INSERT INTO `phieu_xuat` (`ma_px`, `ngay_xuat`, `nguoi_nhan`, `ly_do`, `ma_tk`, `ghi_chu`, `ma_kp`, `so_phieu`, `trang_thai`) VALUES
(1, '2026-10-18 04:13:53.603118', 'Lê Minh Tuấn', NULL, 1, NULL, 1, 'PX-20261018-644', 'XUAT'),
(2, '2026-10-18 15:05:37.144408', 'Lê Minh Tuấn', 'Xuất theo kết hoạch năm', 1, NULL, 2, 'PX-20261018-079', 'XUAT');

-- --------------------------------------------------------

--
-- Table structure for table `san_pham`
--

DROP TABLE IF EXISTS `san_pham`;
CREATE TABLE IF NOT EXISTS `san_pham` (
  `ma_sp` int NOT NULL AUTO_INCREMENT,
  `ten_sp` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `don_vi_tinh` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `muc_ton_toi_thieu` int NOT NULL,
  `muc_ton_toi_da` int NOT NULL,
  `hinh_anh` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trang_thai` tinyint(1) NOT NULL,
  `ma_dm` int DEFAULT NULL,
  `han_su_dung` date DEFAULT NULL,
  PRIMARY KEY (`ma_sp`),
  KEY `san_pham_ma_dm_9759448a` (`ma_dm`)
) ;

--
-- Dumping data for table `san_pham`
--

INSERT INTO `san_pham` (`ma_sp`, `ten_sp`, `don_vi_tinh`, `muc_ton_toi_thieu`, `muc_ton_toi_da`, `hinh_anh`, `trang_thai`, `ma_dm`, `han_su_dung`) VALUES
(1, 'Bút bi Thiên long', 'cái', 5, 1000, '', 1, 1, '2027-10-18'),
(2, 'Bút bi Hồng Hà', 'cái', 5, 1000, '', 1, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tai_khoan`
--

DROP TABLE IF EXISTS `tai_khoan`;
CREATE TABLE IF NOT EXISTS `tai_khoan` (
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `ma_tk` int NOT NULL AUTO_INCREMENT,
  `ten_dang_nhap` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ho_ten` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vai_tro` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `trang_thai` tinyint(1) NOT NULL,
  `ngay_tao` datetime(6) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`ma_tk`),
  UNIQUE KEY `ten_dang_nhap` (`ten_dang_nhap`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tai_khoan`
--

INSERT INTO `tai_khoan` (`password`, `last_login`, `is_superuser`, `ma_tk`, `ten_dang_nhap`, `ho_ten`, `email`, `vai_tro`, `trang_thai`, `ngay_tao`, `is_staff`, `is_active`) VALUES
('pbkdf2_sha256$720000$YBI9ib1nYhMem46hFshGNz$eBDFp08zx4MdHgzedsNNdOlEZBFQWoMBbE/sy0w02Zw=', NULL, 1, 1, 'admin', 'Quản trị viên', 'admin@example.com', 'admin', 1, '2026-10-16 14:34:38.222759', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tai_khoan_groups`
--

DROP TABLE IF EXISTS `tai_khoan_groups`;
CREATE TABLE IF NOT EXISTS `tai_khoan_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `taikhoan_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tai_khoan_groups_taikhoan_id_group_id_a882cb4c_uniq` (`taikhoan_id`,`group_id`),
  KEY `tai_khoan_groups_taikhoan_id_94ef6ec2` (`taikhoan_id`),
  KEY `tai_khoan_groups_group_id_ff99c820` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tai_khoan_user_permissions`
--

DROP TABLE IF EXISTS `tai_khoan_user_permissions`;
CREATE TABLE IF NOT EXISTS `tai_khoan_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `taikhoan_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tai_khoan_user_permissio_taikhoan_id_permission_i_1b41f87a_uniq` (`taikhoan_id`,`permission_id`),
  KEY `tai_khoan_user_permissions_taikhoan_id_ddaef58b` (`taikhoan_id`),
  KEY `tai_khoan_user_permissions_permission_id_55b6ca1a` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
