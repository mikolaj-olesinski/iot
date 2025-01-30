-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sty 30, 2025 at 11:37 AM
-- Wersja serwera: 10.4.28-MariaDB
-- Wersja PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parking`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `companies`
--

CREATE TABLE `companies` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `max_bonus_hours` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `companies`
--

INSERT INTO `companies` (`id`, `name`, `max_bonus_hours`) VALUES
(1, 'ABC Logistics', 10),
(2, 'XYZ Transport', 15),
(3, 'FastCargo', 8),
(8, 'testowa', 5),
(9, 'test', 9);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `parking_entries`
--

CREATE TABLE `parking_entries` (
  `id` int(11) NOT NULL,
  `rfid_tag` varchar(255) NOT NULL,
  `entry_time` datetime NOT NULL,
  `exit_time` datetime DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `duration` decimal(10,2) DEFAULT NULL,
  `company_checkin_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `parking_entries`
--

INSERT INTO `parking_entries` (`id`, `rfid_tag`, `entry_time`, `exit_time`, `total_price`, `duration`, `company_checkin_id`) VALUES
(1, 'FAST002', '2025-01-30 02:42:40', '2025-01-30 03:34:17', NULL, 0.86, NULL),
(5, 'IND001', '2025-01-30 03:40:31', '2025-01-30 03:51:17', NULL, 0.18, NULL),
(7, '12345', '2025-01-30 03:51:10', '2025-01-30 03:51:20', NULL, 0.00, NULL),
(8, '12345', '2025-01-30 03:51:25', '2025-01-30 04:55:13', 20.00, 1.06, NULL),
(9, '111111', '2025-01-30 03:51:29', '2025-01-30 04:56:53', 20.00, 1.09, NULL),
(10, '123', '2025-01-30 04:01:06', '2025-01-30 04:57:54', 10.00, 0.95, NULL),
(11, '12', '2025-01-30 04:05:37', '2025-01-30 04:39:03', NULL, 0.56, 1),
(12, '123456', '2025-01-30 04:18:15', '2025-01-30 04:18:20', NULL, 0.00, NULL),
(17, '12', '2025-01-30 04:56:48', '2025-01-30 05:02:13', 0.00, 0.09, 1),
(18, 'abc', '2025-01-30 04:58:31', '2025-01-30 04:59:24', 10.00, 0.01, NULL),
(19, 'aaa', '2025-01-30 04:58:45', '2025-01-30 05:02:25', 0.00, 0.06, 1),
(20, '1', '2025-01-30 05:02:09', '2025-01-30 05:03:12', 10.00, 0.02, NULL),
(21, '1', '2025-01-30 05:03:22', '2025-01-30 05:11:22', 0.00, 0.13, 1),
(22, '2', '2025-01-30 05:03:24', '2025-01-30 11:11:06', 0.00, 6.13, 1),
(23, '3', '2025-01-30 05:03:26', NULL, NULL, NULL, 1),
(24, '4', '2025-01-30 05:03:28', NULL, NULL, NULL, 2),
(25, '5', '2025-01-30 05:03:30', '2025-01-30 10:40:17', 0.00, 5.61, 2),
(26, '7', '2025-01-30 10:40:29', '2025-01-30 10:58:23', 0.00, 0.30, 1),
(27, '8', '2025-01-30 10:56:37', '2025-01-30 11:35:16', 0.00, 0.64, 1),
(28, '10', '2025-01-30 11:11:12', '2025-01-30 11:32:18', 0.00, 0.35, 1),
(29, '15', '2025-01-30 11:35:10', NULL, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `system_users`
--

CREATE TABLE `system_users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','company_manager','gate_operator') NOT NULL,
  `company_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `system_users`
--

INSERT INTO `system_users` (`id`, `username`, `password`, `role`, `company_id`) VALUES
(1, 'admin', 'admin', 'admin', NULL),
(2, 'gate', 'gate', 'gate_operator', NULL),
(3, 'user', 'user', 'gate_operator', NULL),
(4, 'manager', 'manager', 'company_manager', 1),
(5, 'manager2', 'manager2', 'company_manager', 2),
(6, 'manager_fast', 'fast123', 'company_manager', 3);

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `companies`
--
ALTER TABLE `companies`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `parking_entries`
--
ALTER TABLE `parking_entries`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_parking_entries_rfid` (`rfid_tag`),
  ADD KEY `idx_parking_entries_times` (`entry_time`,`exit_time`);

--
-- Indeksy dla tabeli `system_users`
--
ALTER TABLE `system_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `company_id` (`company_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `companies`
--
ALTER TABLE `companies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `parking_entries`
--
ALTER TABLE `parking_entries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `system_users`
--
ALTER TABLE `system_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `system_users`
--
ALTER TABLE `system_users`
  ADD CONSTRAINT `system_users_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
