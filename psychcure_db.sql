-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 02, 2026 at 09:51 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `psychcure_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `profile_image_url` varchar(255) DEFAULT 'default_profile.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password`, `created_at`, `profile_image_url`) VALUES
(1, 'admin', 'admin123', '2026-03-18 03:45:34', '/static/uploads/profiles/admin_9192a24ca9d74e268e90a1645273f722.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `checkins`
--

CREATE TABLE `checkins` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `mood` varchar(50) NOT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `checkins`
--

INSERT INTO `checkins` (`id`, `student_id`, `mood`, `notes`, `created_at`) VALUES
(8, 5, '😢', 'Stress: 6, Sleep: 8, Energy: 2', '2026-03-23 04:29:41'),
(9, 5, '🙂', 'Stress: 6, Sleep: 7, Energy: 2', '2026-03-29 14:26:29'),
(10, 5, '🙂', 'Stress: 5, Sleep: 7, Energy: 3', '2026-03-29 14:47:04'),
(11, 5, '🙂', 'Stress: 5, Sleep: 7, Energy: 3', '2026-03-30 03:47:17'),
(12, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:05'),
(13, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:12'),
(14, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:13'),
(15, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:13'),
(16, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:14'),
(17, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:14'),
(18, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:15'),
(19, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:15'),
(20, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:15'),
(21, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:15'),
(22, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:15'),
(23, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:15'),
(24, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:16'),
(25, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:16'),
(26, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:16'),
(27, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:16'),
(28, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:16'),
(29, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:16'),
(30, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:17'),
(31, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:17'),
(32, 19, '😊', 'Stress: 10, Sleep: 24, Energy: 1', '2026-03-30 06:32:18'),
(33, 5, '😢', 'Stress: 6, Sleep: 8, Energy: 2', '2026-03-31 04:31:22'),
(34, 5, '😢', 'Stress: 8, Sleep: 9, Energy: 3', '2026-03-31 11:52:26');

-- --------------------------------------------------------

--
-- Table structure for table `counselors`
--

CREATE TABLE `counselors` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `faculty_id` varchar(50) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `profile_image_url` varchar(255) DEFAULT 'default_profile.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `counselors`
--

INSERT INTO `counselors` (`id`, `full_name`, `faculty_id`, `email`, `phone`, `specialization`, `password`, `status`, `created_at`, `profile_image_url`) VALUES
(1, 'pavithra', '123', 'pavithra@gmail.com', '123', 'Psychology', 'Pavi@123', 'active', '2026-03-18 17:46:24', '/static/uploads/profiles/counselor_d9f6a760a6284599a7dd161cc708c4a7.jpg'),
(2, 'Jane ', '1234567', 'psychcure29@gmail.com', '123456789', 'Psychology', 'Counsel123', 'inactive', '2026-03-22 06:38:55', 'default_profile.jpg'),
(3, '1', '1', '1', '1', 'General Counseling', 'Counsel123', 'inactive', '2026-03-30 06:19:51', 'default_profile.jpg'),
(6, 'tejaswini', 'fac1234', 'rsestv@gmail.com', '1234567890', 'Student Welfare', 'Counsel123', 'inactive', '2026-03-30 09:26:37', 'default_profile.jpg'),
(7, 'name', '12345', 'name@gmail.com', '1234567890', 'Psychology', 'vxT#9vl#L', 'active', '2026-03-30 09:39:12', 'default_profile.jpg'),
(14, 'Aruna Dhsjsb', 'Fac12345', 'mudesai09@gmail.com', '1234567890', 'Psychology', 'phO$S5NA%', 'active', '2026-03-31 06:11:57', 'default_profile.jpg'),
(15, 'jane doe', '192210611', 'paruchuripavithra2@gmail.com', '1234567890', 'Student Welfare', 'ZS3r2$agT', 'active', '2026-03-31 06:14:38', 'default_profile.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `exam_plans`
--

CREATE TABLE `exam_plans` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `exam_date` date NOT NULL,
  `stress_level` int(11) NOT NULL,
  `subjects` text NOT NULL,
  `preparation_level` int(11) NOT NULL,
  `stress_message` text DEFAULT NULL,
  `preparation_message` text DEFAULT NULL,
  `plan_message` text DEFAULT NULL,
  `subject_plan` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`subject_plan`)),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `group_announcements`
--

CREATE TABLE `group_announcements` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `counselor_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `group_announcements`
--

INSERT INTO `group_announcements` (`id`, `group_id`, `counselor_id`, `title`, `content`, `created_at`) VALUES
(1, 1, 1, 'ty jv', 'hvvoh', '2026-03-23 04:32:31'),
(2, 1, 1, 'ywhd', 'shsns', '2026-03-29 14:55:42');

-- --------------------------------------------------------

--
-- Table structure for table `group_members`
--

CREATE TABLE `group_members` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `joined_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `group_members`
--

INSERT INTO `group_members` (`id`, `group_id`, `student_id`, `status`, `joined_at`) VALUES
(2, 1, 5, 'approved', '2026-03-23 04:29:59'),
(3, 2, 5, 'approved', '2026-03-23 05:22:26'),
(4, 4, 5, 'approved', '2026-03-24 03:35:52');

-- --------------------------------------------------------

--
-- Table structure for table `group_posts`
--

CREATE TABLE `group_posts` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_type` enum('student','counselor') NOT NULL,
  `content` text NOT NULL,
  `is_pinned` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `group_posts`
--

INSERT INTO `group_posts` (`id`, `group_id`, `user_id`, `user_type`, `content`, `is_pinned`, `created_at`) VALUES
(1, 1, 1, 'counselor', 'v j k', 0, '2026-03-23 04:32:19'),
(2, 1, 5, 'student', 'hejebe', 0, '2026-03-29 14:49:06');

-- --------------------------------------------------------

--
-- Table structure for table `group_tasks`
--

CREATE TABLE `group_tasks` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `counselor_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `task_type` varchar(50) NOT NULL,
  `due_date` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'assigned',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `group_tasks`
--

INSERT INTO `group_tasks` (`id`, `group_id`, `counselor_id`, `title`, `task_type`, `due_date`, `status`, `created_at`) VALUES
(1, 1, 1, 'uuuvih', 'Journal', 'Upcoming', 'assigned', '2026-03-23 04:32:24'),
(2, 1, 1, 'uw7wbs', 'Journal', 'Upcoming', 'assigned', '2026-03-29 14:55:34');

-- --------------------------------------------------------

--
-- Table structure for table `lifestyle`
--

CREATE TABLE `lifestyle` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `sleep_hours` float DEFAULT NULL,
  `exercise_days` int(11) DEFAULT NULL,
  `stress_level` int(11) DEFAULT NULL,
  `mood_score` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lifestyle`
--

INSERT INTO `lifestyle` (`id`, `student_id`, `sleep_hours`, `exercise_days`, `stress_level`, `mood_score`, `created_at`) VALUES
(14, 5, 8, NULL, 6, 2, '2026-03-23 04:29:41'),
(15, 5, 5, NULL, 5, 3, '2026-03-23 04:31:11'),
(16, 5, 7, NULL, 6, 2, '2026-03-29 14:26:29'),
(17, 5, 7, NULL, 5, 3, '2026-03-29 14:47:04'),
(18, 5, 6, NULL, 5, 3, '2026-03-29 14:51:25'),
(19, 5, 7, NULL, 5, 3, '2026-03-30 03:47:17'),
(20, 5, 6, NULL, 5, 3, '2026-03-30 04:19:52'),
(21, 5, 6, NULL, 5, 3, '2026-03-30 04:19:56'),
(22, 5, 4, NULL, 5, 3, '2026-03-30 04:26:53'),
(23, 19, 24, NULL, 10, 1, '2026-03-30 06:32:05'),
(24, 19, 24, NULL, 10, 1, '2026-03-30 06:32:12'),
(25, 19, 24, NULL, 10, 1, '2026-03-30 06:32:13'),
(26, 19, 24, NULL, 10, 1, '2026-03-30 06:32:13'),
(27, 19, 24, NULL, 10, 1, '2026-03-30 06:32:14'),
(28, 19, 24, NULL, 10, 1, '2026-03-30 06:32:14'),
(29, 19, 24, NULL, 10, 1, '2026-03-30 06:32:15'),
(30, 19, 24, NULL, 10, 1, '2026-03-30 06:32:15'),
(31, 19, 24, NULL, 10, 1, '2026-03-30 06:32:15'),
(32, 19, 24, NULL, 10, 1, '2026-03-30 06:32:15'),
(33, 19, 24, NULL, 10, 1, '2026-03-30 06:32:15'),
(34, 19, 24, NULL, 10, 1, '2026-03-30 06:32:15'),
(35, 19, 24, NULL, 10, 1, '2026-03-30 06:32:16'),
(36, 19, 24, NULL, 10, 1, '2026-03-30 06:32:16'),
(37, 19, 24, NULL, 10, 1, '2026-03-30 06:32:16'),
(38, 19, 24, NULL, 10, 1, '2026-03-30 06:32:16'),
(39, 19, 24, NULL, 10, 1, '2026-03-30 06:32:16'),
(40, 19, 24, NULL, 10, 1, '2026-03-30 06:32:16'),
(41, 19, 24, NULL, 10, 1, '2026-03-30 06:32:17'),
(42, 19, 24, NULL, 10, 1, '2026-03-30 06:32:17'),
(43, 19, 24, NULL, 10, 1, '2026-03-30 06:32:18'),
(44, 5, 8, NULL, 6, 2, '2026-03-31 04:31:22'),
(45, 5, 9, NULL, 8, 3, '2026-03-31 11:52:26');

-- --------------------------------------------------------

--
-- Table structure for table `lifestyle_logs`
--

CREATE TABLE `lifestyle_logs` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `sleep_hours` float DEFAULT NULL,
  `bedtime` varchar(20) DEFAULT NULL,
  `screen_time_before_sleep` int(11) DEFAULT NULL,
  `activity_level` varchar(100) DEFAULT NULL,
  `energy_level` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lifestyle_logs`
--

INSERT INTO `lifestyle_logs` (`id`, `student_id`, `sleep_hours`, `bedtime`, `screen_time_before_sleep`, `activity_level`, `energy_level`, `created_at`) VALUES
(27, 5, 5, '11:30 PM', 5, NULL, 3, '2026-03-23 04:31:11'),
(28, 5, NULL, NULL, 4, NULL, NULL, '2026-03-23 04:31:25'),
(29, 5, 6, '11:30 PM', 6, NULL, 3, '2026-03-29 14:51:25'),
(30, 5, NULL, NULL, 6, NULL, NULL, '2026-03-29 14:51:42'),
(31, 5, 6, '11:30 PM', 7, NULL, 3, '2026-03-30 04:19:52'),
(32, 5, 6, '11:30 PM', 7, NULL, 3, '2026-03-30 04:19:56'),
(33, 5, 4, '11:30 PM', 6, NULL, 3, '2026-03-30 04:26:53'),
(34, 5, NULL, NULL, 56, NULL, NULL, '2026-03-30 04:28:21');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_type` enum('student','counselor','admin') NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `user_type`, `title`, `message`, `is_read`, `created_at`) VALUES
(1, 1, 'counselor', 'New Appointment Request', 'pavithra has requested a session on 2026-03-15 at 10:00. Please review and accept or reject.', 0, '2026-03-19 08:17:08'),
(2, 1, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with pavithra on 2026-03-15 at 10:00:00 has been ACCEPTED. Your session is now confirmed.', 1, '2026-03-20 06:16:39'),
(3, 2, 'counselor', 'New Appointment Request', 'sravani has requested a session on 2026-03-16 at 11:30. Please review and accept or reject.', 0, '2026-03-23 04:30:17'),
(4, 5, 'student', 'Group Join Request Update', 'Your request to join stress has been APPROVED.', 0, '2026-03-24 03:32:20'),
(5, 1, 'counselor', 'New Group Join Request', 'sravani has requested to join your group \'46cuv\'. Please review and approve.', 0, '2026-03-24 03:35:52'),
(6, 5, 'student', 'Group Join Request Update', 'Your request to join 46cuv has been APPROVED.', 0, '2026-03-24 03:37:26'),
(7, 2, 'counselor', 'Session Request', 'Student sravani is requesting a session on 2026-03-16 at 11:30. Reason: ', 0, '2026-03-24 04:03:08'),
(8, 1, 'counselor', 'Session Request', 'Student sravani is requesting a session on 2026-03-16 at 11:30. Reason: ', 0, '2026-03-24 04:04:04'),
(9, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with pavithra on 2026-03-16 at 11:30:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-24 04:04:24'),
(10, 5, 'student', 'New Announcement in managing exam anxiety ', 'Your counselor posted a new announcement: ywhd', 0, '2026-03-29 14:55:42'),
(11, 3, 'student', 'Session Booked! ✨', 'Your counselor pavithra booked a session on 25998 at tyi9.', 0, '2026-03-29 14:56:16'),
(12, 1, 'counselor', 'Session Request', 'Student sravani is requesting a session on 2026-03-17 at 10:30:00. Reason: ', 0, '2026-03-30 04:12:57'),
(13, 3, 'counselor', 'Session Request', 'Student 1 is requesting a session on 2026-03-15 at 10:00. Reason: ', 0, '2026-03-30 06:40:31'),
(14, 7, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-03-17 at 10:30:00. Reason: ', 0, '2026-03-30 19:02:37'),
(15, 6, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-03-16 at 09:00:00. Reason: ', 0, '2026-03-30 19:04:40'),
(16, 7, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-03-31 at 10:00. Reason: stress', 0, '2026-03-31 07:16:48'),
(17, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-03-31 at 10:00:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:18:36'),
(18, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-03-31 at 10:00:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:18:38'),
(19, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-03-31 at 10:00:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:18:38'),
(20, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-03-31 at 10:00:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:18:40'),
(21, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-03-31 at 10:00:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:18:41'),
(22, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-03-17 at 10:30:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:18:43'),
(23, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-03-17 at 10:30:00 has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:18:44'),
(24, 5, 'student', 'Appointment Request Declined', 'Your appointment request with name on 2026-03-17 at 10:30:00 was not accepted. Please try booking another slot.', 0, '2026-03-31 07:18:44'),
(25, 7, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-04-01 at 11:00. Reason: stress', 0, '2026-03-31 07:22:06'),
(26, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-04-01 at 11:00:00 (offline) has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:23:22'),
(27, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-04-01 at 11:00:00 (offline) has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:23:26'),
(28, 5, 'student', 'Appointment Request Declined', 'Your appointment request with name on 2026-04-01 at 11:00:00 (offline) was not accepted. Please try booking another slot.', 0, '2026-03-31 07:23:32'),
(29, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-04-01 at 11:00:00 (offline) has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:23:33'),
(30, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-04-01 at 11:00:00 (offline) has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:23:33'),
(31, 5, 'student', 'Appointment Confirmed! ✅', 'Great news! Your appointment with name on 2026-04-01 at 11:00:00 (offline) has been ACCEPTED. Your session is now confirmed.', 0, '2026-03-31 07:23:34'),
(32, 15, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-04-02 at 10:00. Reason: ', 0, '2026-03-31 07:26:17'),
(33, 14, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-04-01 at 11:00. Reason: ', 0, '2026-03-31 07:28:53'),
(34, 1, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-04-01 at 11:00. Reason: ', 0, '2026-03-31 11:50:00'),
(35, 5, 'student', 'Session Request Rejected', 'Your counseling session request with pavithra on 2026-03-17 at 10:30:00 (offline) has been REJECTED. Please try booking another slot or contact support if needed.', 0, '2026-04-01 08:37:50'),
(36, 1, 'counselor', 'Session Request', 'Student pavithra is requesting a session on 2026-04-02 at 10:00. Reason: hwhdbbs', 0, '2026-04-02 06:56:23');

-- --------------------------------------------------------

--
-- Table structure for table `password_resets`
--

CREATE TABLE `password_resets` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `expires_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password_resets`
--

INSERT INTO `password_resets` (`id`, `email`, `code`, `expires_at`, `created_at`) VALUES
(1, 'v@gmial.com', '762286', '2026-03-30 05:57:30', '2026-03-30 05:47:30'),
(2, 'pavigoud29@gmail.com', '537349', '2026-03-31 07:44:40', '2026-03-31 07:34:40');

-- --------------------------------------------------------

--
-- Table structure for table `post_comments`
--

CREATE TABLE `post_comments` (
  `id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_type` enum('student','counselor') NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `post_likes`
--

CREATE TABLE `post_likes` (
  `id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_type` enum('student','counselor') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `risk_alerts`
--

CREATE TABLE `risk_alerts` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `risk_level` enum('low','medium','high','critical') NOT NULL,
  `description` text DEFAULT NULL,
  `status` enum('active','resolved') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `counselor_id` int(11) NOT NULL,
  `session_date` date NOT NULL,
  `session_time` time NOT NULL,
  `reason` text DEFAULT NULL,
  `mode` enum('online','offline') DEFAULT 'offline',
  `status` enum('pending','confirmed','cancelled','completed','rejected') DEFAULT 'pending',
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`id`, `student_id`, `counselor_id`, `session_date`, `session_time`, `reason`, `mode`, `status`, `notes`, `created_at`) VALUES
(3, 5, 2, '2026-03-16', '11:30:00', '', 'offline', 'pending', NULL, '2026-03-23 04:30:17'),
(4, 5, 2, '2026-03-16', '11:30:00', '', 'offline', 'pending', NULL, '2026-03-24 04:03:08'),
(5, 5, 1, '2026-03-16', '11:30:00', '', 'offline', 'confirmed', NULL, '2026-03-24 04:04:04'),
(6, 3, 1, '0000-00-00', '00:00:00', '', 'offline', 'confirmed', NULL, '2026-03-29 14:56:05'),
(7, 5, 1, '2026-03-17', '10:30:00', '', 'offline', 'rejected', NULL, '2026-03-30 04:12:57'),
(8, 19, 3, '2026-03-15', '10:00:00', '', 'offline', 'pending', NULL, '2026-03-30 06:40:31'),
(9, 5, 7, '2026-03-17', '10:30:00', '', 'offline', 'cancelled', NULL, '2026-03-30 19:02:37'),
(10, 5, 6, '2026-03-16', '09:00:00', '', 'offline', 'pending', NULL, '2026-03-30 19:04:40'),
(11, 5, 7, '2026-03-31', '10:00:00', 'stress', 'offline', 'confirmed', NULL, '2026-03-31 07:16:48'),
(12, 5, 7, '2026-04-01', '11:00:00', 'stress', 'offline', 'confirmed', NULL, '2026-03-31 07:22:06'),
(13, 5, 15, '2026-04-02', '10:00:00', '', 'offline', 'pending', NULL, '2026-03-31 07:26:17'),
(14, 5, 14, '2026-04-01', '11:00:00', '', 'offline', 'pending', NULL, '2026-03-31 07:28:53'),
(15, 5, 1, '2026-04-01', '11:00:00', '', 'offline', 'pending', NULL, '2026-03-31 11:50:00'),
(16, 5, 1, '2026-04-02', '10:00:00', 'hwhdbbs', 'offline', 'pending', NULL, '2026-04-02 06:56:23');

-- --------------------------------------------------------

--
-- Table structure for table `session_notes`
--

CREATE TABLE `session_notes` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `counselor_id` int(11) NOT NULL,
  `format` enum('soap','dap','free') NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `college_email` varchar(100) NOT NULL,
  `student_id` varchar(50) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `year` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `profile_image_url` varchar(255) DEFAULT 'default_profile.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `full_name`, `college_email`, `student_id`, `department`, `year`, `phone`, `password`, `status`, `created_at`, `profile_image_url`) VALUES
(2, 'likitha', 'paruchuripavithra2@gmail.com', '12345678', 'Civil Engineering', '3rd Year', '123456789', '1235678', 'approved', '2026-03-20 17:01:32', 'default_profile.jpg'),
(3, 'fufi', 'ufufgig@gmail.co.', '123yu', 'Mechanical Engineering', '3rd Year', '83986858', 'gxyxy', 'rejected', '2026-03-20 17:25:13', 'default_profile.jpg'),
(4, 'ramya', 'ramya@gmail.com', '9877665433', 'Information Technology', '2nd Year', '31649434994', '123', 'approved', '2026-03-20 17:28:25', 'default_profile.jpg'),
(5, 'pavithra', 'pavigoud29@gmail.com', '1234', 'Civil Engineering', '2nd Year', '1234564789', 'Pavi@123', 'approved', '2026-03-22 04:11:46', '/static/uploads/profiles/student_12152df063a04dd992fbd51d7883ddd2.jpg'),
(6, 'john', 'psychcure29@gmail.com', '123456789', 'Information Technology', '3rd Year', '123456789', '12345', 'approved', '2026-03-22 05:48:24', 'default_profile.jpg'),
(14, 'lily', 'lily@gmail.com', 'stu435', 'Computer Science', '3rd Year', '7666589766', 'ZG$f0R$wO', 'approved', '2026-03-30 04:52:34', 'default_profile.jpg'),
(15, 'vinay ', 'vinaykumarreddyramala197gmail.com', 'shsjsi', 'Mechanical Engineering', '2nd Year', '91002604280000000000', '0N9#cK*eP', 'approved', '2026-03-30 05:51:16', 'default_profile.jpg'),
(16, '13455', '1@12', 'fff', 'Mechanical Engineering', '4th Year', '48888888885555555555', '1%4aAQkGy', 'approved', '2026-03-30 06:02:44', 'default_profile.jpg'),
(17, '1', '1', '1', 'Electronics Engineering', '1st Year', '1', '9r5ccHJs^', 'approved', '2026-03-30 06:27:32', 'default_profile.jpg'),
(19, '1', 'worksaveetha@gmail.com', '12', 'Electronics Engineering', '1st Year', '11', 'WxTS#6RuW', 'approved', '2026-03-30 06:28:40', 'default_profile.jpg'),
(20, 'vennala', 'vennal1@gmail.com', 'g', 'Mechanical Engineering', '2nd Year', '1234567890', 'w^OZjiJ&5', 'approved', '2026-03-30 06:58:34', 'default_profile.jpg'),
(21, 'Prasanna', 'prasanna@gmail.com', '123456', 'Civil Engineering', '1st Year', '1234456978', 'nopassword', 'approved', '2026-03-31 05:36:31', 'default_profile.jpg'),
(22, 'Aruna', 'mudesai09@gmail.com', '192210602', 'Computer Science', '1st Year', '1234567890', 'A4Nikxut', 'approved', '2026-03-31 05:40:17', 'default_profile.jpg'),
(23, 'pajsbsb', '1@gmail.com', '1t27w8', 'Civil Engineering', '1st Year', '6184625888', 'nopassword', 'pending', '2026-03-31 08:01:42', 'default_profile.jpg'),
(24, 'ddg', 'ff@d.n', 'rddrfffff4', 'Electronics Engineering', '4th Year', '5255555555', 'nopassword', 'pending', '2026-04-01 07:28:32', 'default_profile.jpg'),
(25, 'qaz', '1@a.b', 'see1233', 'Mechanical Engineering', '4th Year', '1234567890', 'nopassword', 'pending', '2026-04-01 07:32:00', 'default_profile.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `support_groups`
--

CREATE TABLE `support_groups` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `counselor_id` int(11) NOT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `max_students` int(11) DEFAULT 10,
  `frequency` varchar(50) DEFAULT NULL,
  `status` enum('active','closed') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `image_url` varchar(255) DEFAULT 'default_group.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `support_groups`
--

INSERT INTO `support_groups` (`id`, `name`, `description`, `counselor_id`, `tags`, `max_students`, `frequency`, `status`, `created_at`, `image_url`) VALUES
(1, 'managing exam anxiety ', 'stress ', 1, 'Psychology', 15, 'Weekly', 'active', '2026-03-18 17:48:26', 'default_group.jpg'),
(2, 'stress', 'stress', 1, 'Mechanical', 15, 'Weekly', 'active', '2026-03-20 08:29:33', 'default_group.jpg'),
(3, 'stress anxiety ', 'stress', 1, 'Computer Science', 15, 'Weekly', 'active', '2026-03-20 08:55:18', '/static/uploads/groups/group_64d1555cdbd6418696be338a444b0fa2.jpg'),
(4, '46cuv', 'ycubio', 1, 'Mechanical', 15, 'Weekly', 'active', '2026-03-23 04:32:50', 'default_group.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `task_submissions`
--

CREATE TABLE `task_submissions` (
  `id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `submission_text` text NOT NULL,
  `status` varchar(50) DEFAULT 'submitted',
  `submitted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `task_submissions`
--

INSERT INTO `task_submissions` (`id`, `task_id`, `student_id`, `submission_text`, `status`, `submitted_at`) VALUES
(1, 1, 5, 'hvgcynlm', 'submitted', '2026-03-24 07:57:16'),
(2, 2, 5, 'gwhehsbsksn', 'submitted', '2026-03-31 05:55:55');

-- --------------------------------------------------------

--
-- Table structure for table `time_management_plans`
--

CREATE TABLE `time_management_plans` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `classes_per_week` int(11) NOT NULL,
  `pending_assignments` int(11) NOT NULL,
  `study_hours_per_day` float NOT NULL,
  `sleep_hours_per_night` float NOT NULL,
  `workload_status` varchar(50) DEFAULT NULL,
  `suggestions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`suggestions`)),
  `schedule` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`schedule`)),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `time_management_plans`
--

INSERT INTO `time_management_plans` (`id`, `student_id`, `classes_per_week`, `pending_assignments`, `study_hours_per_day`, `sleep_hours_per_night`, `workload_status`, `suggestions`, `schedule`, `created_at`) VALUES
(1, 5, 28, 6, 6, 8, 'Moderate Workload', '[\"Your schedule currently shows a very healthy balance.\"]', '[{\"time\": \"08:00 - 13:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"14:00 - 16:00\", \"task\": \"Assignment Focus (6 pending)\"}, {\"time\": \"16:00 - 19:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"17:00 onwards\", \"task\": \"Sleep cycle (7.9999995h objective)\"}]', '2026-03-29 14:51:06'),
(2, 19, 20, 3, 4, 7, 'Low Workload', '[\"Your schedule currently shows a very healthy balance.\"]', '[{\"time\": \"08:00 - 12:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"13:00 - 14:00\", \"task\": \"Assignment Focus (3 pending)\"}, {\"time\": \"14:00 - 17:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"17:00 onwards\", \"task\": \"Sleep cycle (7.0h objective)\"}]', '2026-03-30 06:38:03'),
(3, 19, 48, 3, 4, 7, 'High Workload', '[\"Your schedule currently shows a very healthy balance.\"]', '[{\"time\": \"08:00 - 17:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"18:00 - 20:00\", \"task\": \"Assignment Focus (3 pending)\"}, {\"time\": \"20:00 - 21:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"17:00 onwards\", \"task\": \"Sleep cycle (7.0h objective)\"}]', '2026-03-30 06:38:18'),
(4, 19, 0, 3, 4, 7, 'Low Workload', '[\"Your schedule currently shows a very healthy balance.\"]', '[{\"time\": \"08:00 - 09:00\", \"task\": \"Assignment Focus (3 pending)\"}, {\"time\": \"09:00 - 12:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"12:00 - 17:00\", \"task\": \"Relaxation & Prep for Tomorrow\"}, {\"time\": \"17:00 onwards\", \"task\": \"Sleep cycle (7.0h objective)\"}]', '2026-03-30 06:38:35'),
(5, 19, 0, 0, 0, 0, 'Low Workload', '[\"To stay alert for 0h of classes/week, try to aim for 7.5h of sleep.\"]', '[{\"time\": \"08:00 - 24:00\", \"task\": \"Relaxation & Prep for Tomorrow\"}, {\"time\": \"24:00 onwards\", \"task\": \"Sleep cycle (0.0h objective)\"}]', '2026-03-30 06:38:44'),
(6, 19, 2, 20, 1, 0, 'High Workload', '[\"With 20 assignments, your 1.0h study time is limited.\", \"To stay alert for 2h of classes/week, try to aim for 7.5h of sleep.\"]', '[{\"time\": \"08:00 - 08:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"09:00 - 10:00\", \"task\": \"Assignment Focus (20 pending)\"}, {\"time\": \"10:00 - 11:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"11:00 - 24:00\", \"task\": \"Relaxation & Prep for Tomorrow\"}, {\"time\": \"24:00 onwards\", \"task\": \"Sleep cycle (0.0h objective)\"}]', '2026-03-30 06:39:09'),
(7, 19, 2, 20, 1, 1, 'High Workload', '[\"With 20 assignments, your 1.0h study time is limited.\", \"To stay alert for 2h of classes/week, try to aim for 7.5h of sleep.\"]', '[{\"time\": \"08:00 - 08:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"09:00 - 10:00\", \"task\": \"Assignment Focus (20 pending)\"}, {\"time\": \"10:00 - 11:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"11:00 - 24:00\", \"task\": \"Relaxation & Prep for Tomorrow\"}, {\"time\": \"24:00 onwards\", \"task\": \"Sleep cycle (0.99999994h objective)\"}]', '2026-03-30 06:39:40'),
(8, 19, 2, 20, 1, 2, 'High Workload', '[\"With 20 assignments, your 1.0h study time is limited.\", \"To stay alert for 2h of classes/week, try to aim for 7.5h of sleep.\"]', '[{\"time\": \"08:00 - 08:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"09:00 - 10:00\", \"task\": \"Assignment Focus (20 pending)\"}, {\"time\": \"10:00 - 11:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"11:00 - 23:00\", \"task\": \"Relaxation & Prep for Tomorrow\"}, {\"time\": \"23:00 onwards\", \"task\": \"Sleep cycle (1.9999999h objective)\"}]', '2026-03-30 06:39:43'),
(9, 5, 20, 3, 4, 7, 'Low Workload', '[\"Your schedule currently shows a very healthy balance.\"]', '[{\"time\": \"08:00 - 12:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"13:00 - 14:00\", \"task\": \"Assignment Focus (3 pending)\"}, {\"time\": \"14:00 - 17:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"17:00 onwards\", \"task\": \"Sleep cycle (7.0h objective)\"}]', '2026-03-31 05:47:07'),
(10, 5, 50, 20, 15, 12, 'High Workload', '[\"Your total daily commitment (25.0h) is very high. Prioritize assignments today.\"]', '[{\"time\": \"08:00 - 18:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"19:00 - 28:00\", \"task\": \"Assignment Focus (20 pending)\"}, {\"time\": \"28:00 - 34:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"12:00 onwards\", \"task\": \"Sleep cycle (12.0h objective)\"}]', '2026-03-31 05:47:18'),
(11, 5, 50, 20, 15, 0, 'High Workload', '[\"Your total daily commitment (25.0h) is very high. Prioritize assignments today.\", \"To stay alert for 50h of classes/week, try to aim for 7.5h of sleep.\"]', '[{\"time\": \"08:00 - 18:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"19:00 - 28:00\", \"task\": \"Assignment Focus (20 pending)\"}, {\"time\": \"28:00 - 34:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"24:00 onwards\", \"task\": \"Sleep cycle (0.0h objective)\"}]', '2026-03-31 05:47:34'),
(12, 5, 0, 20, 15, 0, 'High Workload', '[\"Your total daily commitment (15.0h) is very high. Prioritize assignments today.\", \"To stay alert for 0h of classes/week, try to aim for 7.5h of sleep.\"]', '[{\"time\": \"08:00 - 17:00\", \"task\": \"Assignment Focus (20 pending)\"}, {\"time\": \"17:00 - 23:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"23:00 - 24:00\", \"task\": \"Relaxation & Prep for Tomorrow\"}, {\"time\": \"24:00 onwards\", \"task\": \"Sleep cycle (0.0h objective)\"}]', '2026-03-31 05:47:44'),
(13, 5, 28, 5, 5, 8, 'Moderate Workload', '[\"Your schedule currently shows a very healthy balance.\"]', '[{\"time\": \"08:00 - 13:00\", \"task\": \"University Classes & Lectures\"}, {\"time\": \"14:00 - 15:00\", \"task\": \"Assignment Focus (5 pending)\"}, {\"time\": \"15:00 - 17:00\", \"task\": \"Deep Study/Revision Block\"}, {\"time\": \"17:00 onwards\", \"task\": \"Sleep cycle (7.9999995h objective)\"}]', '2026-03-31 05:54:32');

-- --------------------------------------------------------

--
-- Table structure for table `working_hours`
--

CREATE TABLE `working_hours` (
  `id` int(11) NOT NULL,
  `counselor_id` int(11) NOT NULL,
  `day_of_week` varchar(15) NOT NULL,
  `start_time` time DEFAULT '09:00:00',
  `end_time` time DEFAULT '17:00:00',
  `is_available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `working_hours`
--

INSERT INTO `working_hours` (`id`, `counselor_id`, `day_of_week`, `start_time`, `end_time`, `is_available`) VALUES
(1, 1, 'Monday', '09:00:00', '17:00:00', 1),
(2, 1, 'Tuesday', '09:00:00', '17:00:00', 1),
(3, 1, 'Wednesday', '09:00:00', '17:00:00', 1),
(4, 1, 'Thursday', '09:00:00', '17:00:00', 1),
(5, 1, 'Friday', '09:00:00', '17:00:00', 1),
(6, 1, 'Saturday', '09:00:00', '17:00:00', 1),
(7, 1, 'Sunday', '09:00:00', '17:00:00', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `checkins`
--
ALTER TABLE `checkins`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `counselors`
--
ALTER TABLE `counselors`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `exam_plans`
--
ALTER TABLE `exam_plans`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `group_announcements`
--
ALTER TABLE `group_announcements`
  ADD PRIMARY KEY (`id`),
  ADD KEY `group_id` (`group_id`),
  ADD KEY `counselor_id` (`counselor_id`);

--
-- Indexes for table `group_members`
--
ALTER TABLE `group_members`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_membership` (`group_id`,`student_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `group_posts`
--
ALTER TABLE `group_posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `group_id` (`group_id`);

--
-- Indexes for table `group_tasks`
--
ALTER TABLE `group_tasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `group_id` (`group_id`),
  ADD KEY `counselor_id` (`counselor_id`);

--
-- Indexes for table `lifestyle`
--
ALTER TABLE `lifestyle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `lifestyle_logs`
--
ALTER TABLE `lifestyle_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `post_comments`
--
ALTER TABLE `post_comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_id` (`post_id`);

--
-- Indexes for table `post_likes`
--
ALTER TABLE `post_likes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_like` (`post_id`,`user_id`,`user_type`);

--
-- Indexes for table `risk_alerts`
--
ALTER TABLE `risk_alerts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `counselor_id` (`counselor_id`);

--
-- Indexes for table `session_notes`
--
ALTER TABLE `session_notes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`),
  ADD KEY `counselor_id` (`counselor_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `college_email` (`college_email`),
  ADD UNIQUE KEY `student_id` (`student_id`);

--
-- Indexes for table `support_groups`
--
ALTER TABLE `support_groups`
  ADD PRIMARY KEY (`id`),
  ADD KEY `counselor_id` (`counselor_id`);

--
-- Indexes for table `task_submissions`
--
ALTER TABLE `task_submissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `task_id` (`task_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `time_management_plans`
--
ALTER TABLE `time_management_plans`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `working_hours`
--
ALTER TABLE `working_hours`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `counselor_id` (`counselor_id`,`day_of_week`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `checkins`
--
ALTER TABLE `checkins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `counselors`
--
ALTER TABLE `counselors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `exam_plans`
--
ALTER TABLE `exam_plans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `group_announcements`
--
ALTER TABLE `group_announcements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `group_members`
--
ALTER TABLE `group_members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `group_posts`
--
ALTER TABLE `group_posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `group_tasks`
--
ALTER TABLE `group_tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `lifestyle`
--
ALTER TABLE `lifestyle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `lifestyle_logs`
--
ALTER TABLE `lifestyle_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `password_resets`
--
ALTER TABLE `password_resets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `post_comments`
--
ALTER TABLE `post_comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `post_likes`
--
ALTER TABLE `post_likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `risk_alerts`
--
ALTER TABLE `risk_alerts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `session_notes`
--
ALTER TABLE `session_notes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `support_groups`
--
ALTER TABLE `support_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `task_submissions`
--
ALTER TABLE `task_submissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `time_management_plans`
--
ALTER TABLE `time_management_plans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `working_hours`
--
ALTER TABLE `working_hours`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `checkins`
--
ALTER TABLE `checkins`
  ADD CONSTRAINT `checkins_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `exam_plans`
--
ALTER TABLE `exam_plans`
  ADD CONSTRAINT `exam_plans_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `group_announcements`
--
ALTER TABLE `group_announcements`
  ADD CONSTRAINT `group_announcements_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `support_groups` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `group_announcements_ibfk_2` FOREIGN KEY (`counselor_id`) REFERENCES `counselors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `group_members`
--
ALTER TABLE `group_members`
  ADD CONSTRAINT `group_members_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `support_groups` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `group_members_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `group_posts`
--
ALTER TABLE `group_posts`
  ADD CONSTRAINT `group_posts_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `support_groups` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `group_tasks`
--
ALTER TABLE `group_tasks`
  ADD CONSTRAINT `group_tasks_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `support_groups` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `group_tasks_ibfk_2` FOREIGN KEY (`counselor_id`) REFERENCES `counselors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lifestyle`
--
ALTER TABLE `lifestyle`
  ADD CONSTRAINT `lifestyle_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lifestyle_logs`
--
ALTER TABLE `lifestyle_logs`
  ADD CONSTRAINT `lifestyle_logs_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `post_comments`
--
ALTER TABLE `post_comments`
  ADD CONSTRAINT `post_comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `group_posts` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `post_likes`
--
ALTER TABLE `post_likes`
  ADD CONSTRAINT `post_likes_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `group_posts` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `risk_alerts`
--
ALTER TABLE `risk_alerts`
  ADD CONSTRAINT `risk_alerts_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `sessions`
--
ALTER TABLE `sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sessions_ibfk_2` FOREIGN KEY (`counselor_id`) REFERENCES `counselors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `session_notes`
--
ALTER TABLE `session_notes`
  ADD CONSTRAINT `session_notes_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `session_notes_ibfk_2` FOREIGN KEY (`counselor_id`) REFERENCES `counselors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `support_groups`
--
ALTER TABLE `support_groups`
  ADD CONSTRAINT `support_groups_ibfk_1` FOREIGN KEY (`counselor_id`) REFERENCES `counselors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `task_submissions`
--
ALTER TABLE `task_submissions`
  ADD CONSTRAINT `task_submissions_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `group_tasks` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `task_submissions_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `time_management_plans`
--
ALTER TABLE `time_management_plans`
  ADD CONSTRAINT `time_management_plans_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `working_hours`
--
ALTER TABLE `working_hours`
  ADD CONSTRAINT `working_hours_ibfk_1` FOREIGN KEY (`counselor_id`) REFERENCES `counselors` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
