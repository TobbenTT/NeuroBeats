-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2025 a las 22:22:36
-- Versión del servidor: 11.8.5-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `neurobeats_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
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
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add genre', 7, 'add_genre'),
(26, 'Can change genre', 7, 'change_genre'),
(27, 'Can delete genre', 7, 'delete_genre'),
(28, 'Can view genre', 7, 'view_genre'),
(29, 'Can add song', 8, 'add_song'),
(30, 'Can change song', 8, 'change_song'),
(31, 'Can delete song', 8, 'delete_song'),
(32, 'Can view song', 8, 'view_song'),
(33, 'Can add rating', 9, 'add_rating'),
(34, 'Can change rating', 9, 'change_rating'),
(35, 'Can delete rating', 9, 'delete_rating'),
(36, 'Can view rating', 9, 'view_rating'),
(37, 'Can add favorite', 10, 'add_favorite'),
(38, 'Can change favorite', 10, 'change_favorite'),
(39, 'Can delete favorite', 10, 'delete_favorite'),
(40, 'Can view favorite', 10, 'view_favorite'),
(41, 'Can add badge', 11, 'add_badge'),
(42, 'Can change badge', 11, 'change_badge'),
(43, 'Can delete badge', 11, 'delete_badge'),
(44, 'Can view badge', 11, 'view_badge'),
(45, 'Can add profile', 12, 'add_profile'),
(46, 'Can change profile', 12, 'change_profile'),
(47, 'Can delete profile', 12, 'delete_profile'),
(48, 'Can view profile', 12, 'view_profile'),
(49, 'Can add comment', 13, 'add_comment'),
(50, 'Can change comment', 13, 'change_comment'),
(51, 'Can delete comment', 13, 'delete_comment'),
(52, 'Can view comment', 13, 'view_comment');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$d3LeVh0KNbtmQ31AgBmk29$2Qeb9wd7wD0ad2Ceb2g9S4r0aEdZm/Tbwqemaw1baAU=', '2025-12-03 21:57:16.755610', 1, 'tobben', '', '', 'tobben@gmail.com', 1, 1, '2025-12-02 21:03:36.979954'),
(2, 'pbkdf2_sha256$1000000$U4BDgoJtWejKezbUTXYEVM$y8uBFpXjx8oFeWiIK4ftK/7HxjyfQUgpaFdcSAF9UzQ=', '2025-12-03 01:10:19.333050', 0, 'Kiwi', '', '', '', 0, 1, '2025-12-03 00:10:54.000000'),
(3, 'pbkdf2_sha256$1000000$99cF00vgLH4Q0OikcTv1AE$rBu5zFt0fwTBv0sgKjnB6dQ3YGwe7hWRLDfq6CB2lkw=', '2025-12-03 23:27:58.009618', 0, 'Pipe', '', '', '', 0, 1, '2025-12-03 00:52:18.891918'),
(4, 'pbkdf2_sha256$1000000$SdtRk1TrK36VkIAWZHsnIG$prnhbQ5cBxZdNG/ySyDBmnPmo30nlzumTBzQi00Gn0o=', '2025-12-03 01:01:33.944894', 0, 'Kafka', '', '', '', 0, 1, '2025-12-03 01:00:52.867355'),
(5, 'pbkdf2_sha256$1000000$2XPJLsjLXwuBeqOK0ggmpz$cAG5l1qByJYNLdeRP+/e4xZXPyy3Rt+JRfpXJFJDzQs=', '2025-12-03 01:43:20.160429', 0, 'Tongo', '', '', '', 0, 1, '2025-12-03 01:39:00.196860'),
(6, 'pbkdf2_sha256$1000000$i0upqIg3SO6wrHvlgAOgwH$Cjh5J7rUew6UNFOs2Ahg0iiUpKGpQ2CxdOWteJ4YM4Y=', '2025-12-03 21:11:27.522872', 0, 'Miky', '', '', '', 0, 1, '2025-12-03 02:23:02.876060'),
(7, 'pbkdf2_sha256$1000000$Raand0Qx98oVDP6JYeTiig$CVeQs5uwEo1woeXHBj4A44zyg2l7hoq9Uz+uGU1ffUg=', '2025-12-03 17:23:55.131991', 0, 'tobby', '', '', '', 0, 1, '2025-12-03 17:23:46.012586'),
(8, 'pbkdf2_sha256$1000000$dWLEAywLZyIE475a3lFl0f$9bogWBFaG/Fz/q30uM20lTTcC54ABZOgx/Kq6jJznP0=', NULL, 0, 'Ale', '', '', '', 0, 1, '2025-12-03 20:59:04.948212'),
(9, 'pbkdf2_sha256$1000000$AB4AADb5DqZY4zdXtKMhKd$PJE4Kf6L2OAdOkrgBG9lnrRTCk42CdR/EUtvL/+APLA=', NULL, 0, 'Darcko', '', '', '', 0, 1, '2025-12-03 23:19:31.009630'),
(10, 'pbkdf2_sha256$1000000$e6ynSnVyFNwj1CIS4w7AcD$OxmuWlv/AFhfs4AbsIWEWtNb5eCRC3NPWFOJS0EQaSA=', NULL, 0, 'Rubius', '', '', '', 0, 1, '2025-12-04 17:12:06.458077');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-12-02 22:41:57.349907', '1', 'Pop', 1, '[{\"added\": {}}]', 7, 1),
(2, '2025-12-02 22:42:01.335473', '2', 'Jazz', 1, '[{\"added\": {}}]', 7, 1),
(3, '2025-12-02 22:42:04.419548', '3', 'Electrónica', 1, '[{\"added\": {}}]', 7, 1),
(4, '2025-12-02 22:42:06.943621', '4', 'Hip Hop', 1, '[{\"added\": {}}]', 7, 1),
(5, '2025-12-02 22:42:12.061515', '5', 'K-pop', 1, '[{\"added\": {}}]', 7, 1),
(6, '2025-12-02 22:42:17.241345', '6', 'J-pop', 1, '[{\"added\": {}}]', 7, 1),
(7, '2025-12-03 00:59:00.841718', '2', 'Kiwi', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 4, 1),
(8, '2025-12-03 01:25:38.886446', '7', 'pop latino', 1, '[{\"added\": {}}]', 7, 1),
(9, '2025-12-03 01:25:55.588454', '8', 'balada romántica', 1, '[{\"added\": {}}]', 7, 1),
(10, '2025-12-03 01:26:02.310023', '9', 'pop rock', 1, '[{\"added\": {}}]', 7, 1),
(11, '2025-12-03 01:26:09.016137', '10', 'Romance', 1, '[{\"added\": {}}]', 7, 1),
(12, '2025-12-03 01:29:15.606044', '11', 'Trap', 1, '[{\"added\": {}}]', 7, 1),
(13, '2025-12-03 01:50:35.722419', '12', 'metal', 1, '[{\"added\": {}}]', 7, 1),
(14, '2025-12-03 01:50:38.771516', '13', 'rock', 1, '[{\"added\": {}}]', 7, 1),
(15, '2025-12-03 01:50:44.436765', '14', 'rap', 1, '[{\"added\": {}}]', 7, 1),
(16, '2025-12-03 01:52:42.703463', '15', 'indie', 1, '[{\"added\": {}}]', 7, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(13, 'music', 'comment'),
(10, 'music', 'favorite'),
(7, 'music', 'genre'),
(9, 'music', 'rating'),
(8, 'music', 'song'),
(6, 'sessions', 'session'),
(11, 'users', 'badge'),
(12, 'users', 'profile');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-12-02 21:01:57.735057'),
(2, 'auth', '0001_initial', '2025-12-02 21:01:57.929899'),
(3, 'admin', '0001_initial', '2025-12-02 21:01:57.968521'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-12-02 21:01:57.973521'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-02 21:01:57.980523'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-12-02 21:01:58.018126'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-12-02 21:01:58.039856'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-12-02 21:01:58.054857'),
(9, 'auth', '0004_alter_user_username_opts', '2025-12-02 21:01:58.058856'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-12-02 21:01:58.080861'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-12-02 21:01:58.081860'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-12-02 21:01:58.085863'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-12-02 21:01:58.099373'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-12-02 21:01:58.115379'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-12-02 21:01:58.128597'),
(16, 'auth', '0011_update_proxy_permissions', '2025-12-02 21:01:58.133599'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-12-02 21:01:58.147100'),
(18, 'music', '0001_initial', '2025-12-02 21:01:58.316644'),
(19, 'sessions', '0001_initial', '2025-12-02 21:01:58.331948'),
(20, 'users', '0001_initial', '2025-12-02 22:31:25.965166'),
(21, 'music', '0002_song_is_private', '2025-12-03 16:53:21.851626'),
(22, 'music', '0003_alter_genre_name_alter_rating_score_alter_song_title', '2025-12-03 17:07:22.355208'),
(23, 'users', '0002_profile_is_private', '2025-12-03 17:26:05.898067'),
(24, 'music', '0004_comment', '2025-12-03 17:45:53.099328'),
(25, 'music', '0005_song_bpm_song_energy', '2025-12-03 17:53:16.595884'),
(26, 'music', '0006_song_full_audio_file', '2025-12-04 16:56:40.142181');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('9y9eqpo4aaw7ek7qua3zdgveot7921iq', '.eJxVjDsOwjAQBe_iGln-fyjpOYPl9a5xADlSnFSIu0OkFNC-mXkvlvK2trQNWtKE7MwkO_1ukMuD-g7wnvtt5mXu6zIB3xV-0MGvM9Lzcrh_By2P9q2trRB8QJTCVu2lx5BRI3kgI4QJ4KK2ykQVCKJXiBoqOeepRotFB_b-AOBQN_g:1vQYw9:k9RC3tuvrbwcMCLqM2W5tBlyM4LGvyfTuCnHIlaiPkQ', '2025-12-16 22:33:33.900511'),
('ddaxw1bjk9y63e7qa8fvs5nbgvlbsaxc', '.eJxVjDsOwjAQBe_iGln-fyjpOYPl9a5xADlSnFSIu0OkFNC-mXkvlvK2trQNWtKE7MwkO_1ukMuD-g7wnvtt5mXu6zIB3xV-0MGvM9Lzcrh_By2P9q2trRB8QJTCVu2lx5BRI3kgI4QJ4KK2ykQVCKJXiBoqOeepRotFB_b-AOBQN_g:1vQbMn:3b0EQS7eQkDt59TZEDKpXdWa4yplpLpb6_oSf-t1x9Q', '2025-12-17 01:09:13.613983'),
('dxkyy06vcc5zyclu12g3tm4nmwl55br5', '.eJxVjEsOAiEQBe_C2hB-toxL956BNHQjowaSYWZlvLuSzEK3VfXeSwTc1hK2zkuYSZwFiMMvi5geXIegO9Zbk6nVdZmjHIncbZfXRvy87O3fQcFexvpoktM-uRgNK84OIGecTLYaI7npxIoYktEKQDviL8oWPDuridBr8f4A_qE4Yg:1vQu8F:3cun73dMKYtLb6GCH5pQKssPmewvzjv5iyuGXBbzTpw', '2025-12-17 21:11:27.524872'),
('e0xfnli1fvdtgyzstgfe35moqr73szkb', '.eJxVjDsOwjAQBe_iGln-fyjpOYPl9a5xADlSnFSIu0OkFNC-mXkvlvK2trQNWtKE7MwkO_1ukMuD-g7wnvtt5mXu6zIB3xV-0MGvM9Lzcrh_By2P9q2trRB8QJTCVu2lx5BRI3kgI4QJ4KK2ykQVCKJXiBoqOeepRotFB_b-AOBQN_g:1vQuqa:zPVptNIZvJrp7a1GK2Q74Y3SqfdBmWo3wrgc8sXBKMM', '2025-12-17 21:57:16.756616'),
('eo5e7cwmct822bljn5tevogew899a951', '.eJxVjE0OwiAYBe_C2hAoAYpL956BfH9I1dCktCvj3bVJF7p9M_NeKsO21rx1WfLE6qy8Ov1uCPSQtgO-Q7vNmua2LhPqXdEH7fo6szwvh_t3UKHXb12YvYkeYwHnwcZoWCIYBwksYXLGphgslQQjoSOPLDIYCmHg4smN6v0B-sA4jA:1vQbto:8Yj-TWWGcLWrrEj58Lw6zzPfxuynFRCaIVBF54O-oVw', '2025-12-17 01:43:20.164952'),
('f7k1mtxyurbs7ohxh6n5c9dhfqr7s2gh', '.eJxVjDsOwjAQBe_iGln-fyjpOYPl9a5xADlSnFSIu0OkFNC-mXkvlvK2trQNWtKE7MwkO_1ukMuD-g7wnvtt5mXu6zIB3xV-0MGvM9Lzcrh_By2P9q2trRB8QJTCVu2lx5BRI3kgI4QJ4KK2ykQVCKJXiBoqOeepRotFB_b-AOBQN_g:1vQtk7:VOg_likqzm4i7UOEebpbWSwe73qMUbBp9F9Qn8SExw4', '2025-12-17 20:46:31.284774'),
('s7jwf2p4smq4vxkcjd3cc9fol7vw2lti', '.eJxVjDsOwjAQBe_iGln-fyjpOYPl9a5xADlSnFSIu0OkFNC-mXkvlvK2trQNWtKE7MwkO_1ukMuD-g7wnvtt5mXu6zIB3xV-0MGvM9Lzcrh_By2P9q2trRB8QJTCVu2lx5BRI3kgI4QJ4KK2ykQVCKJXiBoqOeepRotFB_b-AOBQN_g:1vQqKl:i1IrLmS852xSNVFACtKjht1PYhQk4kVqDNveKs2u5Gs', '2025-12-17 17:08:07.920017'),
('u4d5qgcrggygi1kxk1haqkk7ao2lr81g', '.eJxVjDsOwjAQBe_iGln-rT-U9DmDtc7aOIBiKU4qxN1JpBTQvpl5bxZxW2vcel7iROzKFLv8bgnHZ54PQA-c742PbV6XKfFD4SftfGiUX7fT_Tuo2OteF2mAvAeLWpFwiQJJIxxAkaNEHXzONngJARzsUKHPSSktAAzZQIV9vsgRNys:1vQbNr:LQyhmU5beg1VgLIVmDTmOln_xtLaujqsGry2I9anYC0', '2025-12-17 01:10:19.334050'),
('v7potp9ya1zugo17jml7cjt23d259oz0', '.eJxVjEsOwjAMBe-SNYoaO3IpS_acIXLsmBRQK_WzQtydVuoCtm9m3tslXpea1rlMqVd3cehOv1tmeZZhB_rg4T56GYdl6rPfFX_Q2d9GLa_r4f4dVJ7rVlPORdGo04ZLi2BEVII0ATrSs5kYgcSWNwoYEcBQIgA2QgqMwX2--gQ37A:1vQwGM:zwwYJW5zmVk5wkYtBSEpNqLGcZD41VVmXglMjPkGCa0', '2025-12-17 23:27:58.011618'),
('w725g9g90v73v5gi0757wyoimauxz394', '.eJxVjDsOwjAQBe_iGln-fyjpOYPl9a5xADlSnFSIu0OkFNC-mXkvlvK2trQNWtKE7MwkO_1ukMuD-g7wnvtt5mXu6zIB3xV-0MGvM9Lzcrh_By2P9q2trRB8QJTCVu2lx5BRI3kgI4QJ4KK2ykQVCKJXiBoqOeepRotFB_b-AOBQN_g:1vQrAS:gDqqKGCnbeK506hdky9zliCZ70_ZwUJTOGWQfv_CvZE', '2025-12-17 18:01:32.513653');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `music_comment`
--

CREATE TABLE `music_comment` (
  `id` bigint(20) NOT NULL,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `song_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `music_comment`
--

INSERT INTO `music_comment` (`id`, `text`, `created_at`, `song_id`, `user_id`) VALUES
(1, 'Goat', '2025-12-03 21:18:17.753705', 17, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `music_favorite`
--

CREATE TABLE `music_favorite` (
  `id` bigint(20) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `song_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `music_favorite`
--

INSERT INTO `music_favorite` (`id`, `added_at`, `user_id`, `song_id`) VALUES
(9, '2025-12-03 18:51:55.232020', 1, 17),
(12, '2025-12-03 23:24:50.992168', 1, 34);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `music_genre`
--

CREATE TABLE `music_genre` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `music_genre`
--

INSERT INTO `music_genre` (`id`, `name`) VALUES
(8, 'balada romántica'),
(3, 'Electrónica'),
(4, 'Hip Hop'),
(15, 'indie'),
(6, 'J-pop'),
(2, 'Jazz'),
(5, 'K-pop'),
(12, 'metal'),
(1, 'Pop'),
(7, 'pop latino'),
(9, 'pop rock'),
(14, 'rap'),
(13, 'rock'),
(10, 'Romance'),
(11, 'Trap');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `music_rating`
--

CREATE TABLE `music_rating` (
  `id` bigint(20) NOT NULL,
  `score` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `song_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `music_rating`
--

INSERT INTO `music_rating` (`id`, `score`, `user_id`, `song_id`) VALUES
(6, 5, 1, 17),
(8, 5, 1, 34);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `music_song`
--

CREATE TABLE `music_song` (
  `id` bigint(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `artist` varchar(100) NOT NULL,
  `cover_image` varchar(100) NOT NULL,
  `audio_file` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `genre_id` bigint(20) DEFAULT NULL,
  `uploader_id` int(11) NOT NULL,
  `is_private` tinyint(1) NOT NULL,
  `bpm` int(11) DEFAULT NULL,
  `energy` double DEFAULT NULL,
  `full_audio_file` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `music_song`
--

INSERT INTO `music_song` (`id`, `title`, `artist`, `cover_image`, `audio_file`, `created_at`, `genre_id`, `uploader_id`, `is_private`, `bpm`, `energy`, `full_audio_file`) VALUES
(17, 'Magic', 'Ado', 'covers/AdoLuche3.jpg', 'tracks/cut_d1e0a7ec_【Ado】MAGIC.flac', '2025-12-03 18:33:06.807852', 6, 1, 0, 89, 0.3918, NULL),
(34, 'Besame', 'Camila', 'covers/WhatsApp_Image_2025-12-03_at_18.47.18.jpeg', 'tracks/cut_4da445cc_Camila — Bésame [Letra].flac', '2025-12-03 23:17:02.356841', 8, 1, 0, 172, 0.1864, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_badge`
--

CREATE TABLE `users_badge` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `icon_name` varchar(50) NOT NULL,
  `criteria` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users_badge`
--

INSERT INTO `users_badge` (`id`, `name`, `description`, `icon_name`, `criteria`) VALUES
(1, 'Productor', 'Creador de contenido (1+ Subida)', 'fas fa-upload', 'productor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_profile`
--

CREATE TABLE `users_profile` (
  `id` bigint(20) NOT NULL,
  `bio` longtext NOT NULL,
  `avatar` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_private` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users_profile`
--

INSERT INTO `users_profile` (`id`, `bio`, `avatar`, `user_id`, `is_private`) VALUES
(1, 'Puto el que lo lea', 'avatars/AdoLuche3_iOPgTkI.jpg', 1, 1),
(2, '', 'avatars/AdoLuche2.jpg', 2, 0),
(3, '', 'avatars/default.jpg', 3, 0),
(4, '', 'avatars/default.jpg', 4, 0),
(5, '', 'avatars/snapedit_1761379766148.jpg', 5, 0),
(6, 'Mikii', 'avatars/256c6b27002508a215566a5d8be0f9bf.jpg', 6, 0),
(7, '', 'avatars/AdoLuche.jpg', 7, 1),
(8, '', 'avatars/default.jpg', 8, 0),
(9, '', 'avatars/default.jpg', 9, 0),
(10, '', 'avatars/default.jpg', 10, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_profile_badges`
--

CREATE TABLE `users_profile_badges` (
  `id` bigint(20) NOT NULL,
  `profile_id` bigint(20) NOT NULL,
  `badge_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users_profile_badges`
--

INSERT INTO `users_profile_badges` (`id`, `profile_id`, `badge_id`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 5, 1),
(4, 6, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_profile_follows`
--

CREATE TABLE `users_profile_follows` (
  `id` bigint(20) NOT NULL,
  `from_profile_id` bigint(20) NOT NULL,
  `to_profile_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users_profile_follows`
--

INSERT INTO `users_profile_follows` (`id`, `from_profile_id`, `to_profile_id`) VALUES
(2, 1, 2),
(3, 1, 5),
(1, 2, 1),
(4, 5, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `music_comment`
--
ALTER TABLE `music_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `music_comment_song_id_ca79f133_fk_music_song_id` (`song_id`),
  ADD KEY `music_comment_user_id_0d3cd408_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `music_favorite`
--
ALTER TABLE `music_favorite`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `music_favorite_user_id_song_id_7c6d9309_uniq` (`user_id`,`song_id`),
  ADD KEY `music_favorite_song_id_9605dbb3_fk_music_song_id` (`song_id`);

--
-- Indices de la tabla `music_genre`
--
ALTER TABLE `music_genre`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `music_rating`
--
ALTER TABLE `music_rating`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `music_rating_user_id_song_id_daeef630_uniq` (`user_id`,`song_id`),
  ADD KEY `music_rating_song_id_9058e1cb_fk_music_song_id` (`song_id`);

--
-- Indices de la tabla `music_song`
--
ALTER TABLE `music_song`
  ADD PRIMARY KEY (`id`),
  ADD KEY `music_song_genre_id_6726859e_fk_music_genre_id` (`genre_id`),
  ADD KEY `music_song_uploader_id_dba164c1_fk_auth_user_id` (`uploader_id`);

--
-- Indices de la tabla `users_badge`
--
ALTER TABLE `users_badge`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users_profile`
--
ALTER TABLE `users_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indices de la tabla `users_profile_badges`
--
ALTER TABLE `users_profile_badges`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_profile_badges_profile_id_badge_id_5bc2d295_uniq` (`profile_id`,`badge_id`),
  ADD KEY `users_profile_badges_badge_id_756bec36_fk_users_badge_id` (`badge_id`);

--
-- Indices de la tabla `users_profile_follows`
--
ALTER TABLE `users_profile_follows`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_profile_follows_from_profile_id_to_profi_1c65739f_uniq` (`from_profile_id`,`to_profile_id`),
  ADD KEY `users_profile_follows_to_profile_id_4cbc763c_fk_users_profile_id` (`to_profile_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `music_comment`
--
ALTER TABLE `music_comment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `music_favorite`
--
ALTER TABLE `music_favorite`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `music_genre`
--
ALTER TABLE `music_genre`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `music_rating`
--
ALTER TABLE `music_rating`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `music_song`
--
ALTER TABLE `music_song`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `users_badge`
--
ALTER TABLE `users_badge`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `users_profile`
--
ALTER TABLE `users_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `users_profile_badges`
--
ALTER TABLE `users_profile_badges`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `users_profile_follows`
--
ALTER TABLE `users_profile_follows`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `music_comment`
--
ALTER TABLE `music_comment`
  ADD CONSTRAINT `music_comment_song_id_ca79f133_fk_music_song_id` FOREIGN KEY (`song_id`) REFERENCES `music_song` (`id`),
  ADD CONSTRAINT `music_comment_user_id_0d3cd408_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `music_favorite`
--
ALTER TABLE `music_favorite`
  ADD CONSTRAINT `music_favorite_song_id_9605dbb3_fk_music_song_id` FOREIGN KEY (`song_id`) REFERENCES `music_song` (`id`),
  ADD CONSTRAINT `music_favorite_user_id_c2a25ff3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `music_rating`
--
ALTER TABLE `music_rating`
  ADD CONSTRAINT `music_rating_song_id_9058e1cb_fk_music_song_id` FOREIGN KEY (`song_id`) REFERENCES `music_song` (`id`),
  ADD CONSTRAINT `music_rating_user_id_573020d2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `music_song`
--
ALTER TABLE `music_song`
  ADD CONSTRAINT `music_song_genre_id_6726859e_fk_music_genre_id` FOREIGN KEY (`genre_id`) REFERENCES `music_genre` (`id`),
  ADD CONSTRAINT `music_song_uploader_id_dba164c1_fk_auth_user_id` FOREIGN KEY (`uploader_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `users_profile`
--
ALTER TABLE `users_profile`
  ADD CONSTRAINT `users_profile_user_id_2112e78d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `users_profile_badges`
--
ALTER TABLE `users_profile_badges`
  ADD CONSTRAINT `users_profile_badges_badge_id_756bec36_fk_users_badge_id` FOREIGN KEY (`badge_id`) REFERENCES `users_badge` (`id`),
  ADD CONSTRAINT `users_profile_badges_profile_id_42264737_fk_users_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `users_profile` (`id`);

--
-- Filtros para la tabla `users_profile_follows`
--
ALTER TABLE `users_profile_follows`
  ADD CONSTRAINT `users_profile_follow_from_profile_id_ece05f14_fk_users_pro` FOREIGN KEY (`from_profile_id`) REFERENCES `users_profile` (`id`),
  ADD CONSTRAINT `users_profile_follows_to_profile_id_4cbc763c_fk_users_profile_id` FOREIGN KEY (`to_profile_id`) REFERENCES `users_profile` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
