-- phpMyAdmin SQL Dump
-- version 4.8.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 30, 2018 at 06:23 PM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 5.6.35

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `atria_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `session_db`
--

CREATE TABLE `session_db` (
  `userid` int(5) NOT NULL,
  `login_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `logout_check` int(2) NOT NULL DEFAULT '0',
  `logout_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(5) NOT NULL,
  `username` varchar(50) NOT NULL,
  `usn` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `email_verified` int(2) NOT NULL DEFAULT '0',
  `password` varchar(200) NOT NULL,
  `register_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `verification_code` varchar(10) DEFAULT NULL,
  `verification_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `usn`, `email`, `email_verified`, `password`, `register_time`, `verification_code`, `verification_time`) VALUES
(4, 'John', '1AT15IS090', 'shep.maksim@0nly.org', 0, '$5$rounds=535000$FQScT8fdXXxo8pH3$lMsMouI1Dm4ssc9FWvbfl6DLjGTQSdBlip2bhcp0x84', '2018-04-30 13:02:48', '2xr32fCz7q', '2018-04-30 13:04:19'),
(5, 'xyzzz', '1AT15IS091', 'tagg.zerek@0nly.org', 0, '$5$rounds=535000$4cMmnhda69QQI9jZ$53HvDHWTzlmT3cRhu6VUFbJ8CZCMK9QzogfeLxFcDx.', '2018-04-30 13:49:56', 'qsmxoFKLjM', '2018-04-28 13:50:11'),
(6, 'Sujith Menon', '1AT15IS092', 'alexcardinal22@gmail.com', 0, '$5$rounds=535000$ZyBvm6yrbiYM5v3I$5M8Jax0ialgHVr80AfUb45tUpoefLENj.cZ6TIA3g90', '2018-04-30 14:34:19', 'mpW1eYtKPS', '2018-04-30 13:26:52'),
(7, 'Shashank P', '1AT15IS081', 'shashank.prakash1997@gmail.com', 0, '$5$rounds=535000$S1SNr3djFlA9DouB$V0tg1ibyY3QV.QCsOV8mPYNNO8hqNXcGgdHPAcKIap6', '2018-04-30 15:50:58', 'pIxklvRdKK', '2018-04-30 13:51:39');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `session_db`
--
ALTER TABLE `session_db`
  ADD UNIQUE KEY `userid` (`userid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `usn` (`usn`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `session_db`
--
ALTER TABLE `session_db`
  ADD CONSTRAINT `USERID` FOREIGN KEY (`userid`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
