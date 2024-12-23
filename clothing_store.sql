-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Feb 16, 2024 at 01:14 PM
-- Server version: 11.2.2-MariaDB
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clothing_store`
--
CREATE DATABASE IF NOT EXISTS `clothing_store` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `clothing_store`;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_addresses`
--

DROP TABLE IF EXISTS `tbl_addresses`;
CREATE TABLE IF NOT EXISTS `tbl_addresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` tinytext NOT NULL,
  `full` tinytext NOT NULL,
  `city` tinytext NOT NULL,
  `state` tinytext NOT NULL,
  `pincode` int(11) NOT NULL,
  `contact` varchar(10) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_addresses`
--

INSERT INTO `tbl_addresses` (`id`, `title`, `full`, `city`, `state`, `pincode`, `contact`, `user_id`) VALUES
(1, 'Home', '123, ABC Road, Kolhapur, Maharashtra, India.', 'Kolhapur', 'Maharashtra', 416012, '9168242081', 1),
(2, 'Office', 'test 1233', 'Kop', 'Maharashtra', 416008, '9028829392', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_cart`
--

DROP TABLE IF EXISTS `tbl_cart`;
CREATE TABLE IF NOT EXISTS `tbl_cart` (
  `product_info` text NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_cart`
--

INSERT INTO `tbl_cart` (`product_info`, `user_id`, `date`) VALUES
('[{\"spec\": \"28\", \"color\": \"Black\", \"qnt\": 1}, {\"spec\": \"22\", \"color\": \"Brown\", \"qnt\": 1}, {\"spec\": \"30\", \"color\": \"Blue\", \"qnt\": 1}]', 1, '2024-02-16 13:12:55');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_categories`
--

DROP TABLE IF EXISTS `tbl_categories`;
CREATE TABLE IF NOT EXISTS `tbl_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` tinytext NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_categories`
--

INSERT INTO `tbl_categories` (`id`, `title`, `date`) VALUES
(1, 'T-shirt', '2024-02-11 04:19:55'),
(2, 'Shirt', '2024-02-11 04:19:55'),
(3, 'Joggers', '2024-02-11 04:19:55'),
(4, 'Trousers', '2024-02-11 04:19:55'),
(5, 'Jeans', '2024-02-11 04:19:55'),
(6, 'Hoodie', '2024-02-11 04:19:55'),
(7, 'Sweatshirt', '2024-02-11 04:19:55');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_orders`
--

DROP TABLE IF EXISTS `tbl_orders`;
CREATE TABLE IF NOT EXISTS `tbl_orders` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` tinytext NOT NULL,
  `order_user` int(11) DEFAULT NULL,
  `order_total` float NOT NULL,
  `order_shipto` int(11) DEFAULT NULL,
  `order_payment_mode` enum('Pay On Delivery','UPI') NOT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`order_id`),
  KEY `order_user` (`order_user`),
  KEY `order_shipto` (`order_shipto`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_orders`
--

INSERT INTO `tbl_orders` (`order_id`, `order_no`, `order_user`, `order_total`, `order_shipto`, `order_payment_mode`, `order_date`) VALUES
(1, 'e29f8a7b-ccac-11ee-ad0b-fcaa145471b4', 1, 2498, 1, 'Pay On Delivery', '2024-02-16 09:22:20'),
(2, '456a3d39-ccad-11ee-b2c6-fcaa145471b4', 1, 3897, 2, 'Pay On Delivery', '2024-02-16 09:25:06');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_order_details`
--

DROP TABLE IF EXISTS `tbl_order_details`;
CREATE TABLE IF NOT EXISTS `tbl_order_details` (
  `order_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_quantity` int(11) NOT NULL,
  `product_color` varchar(255) NOT NULL,
  `product_total` float NOT NULL,
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_order_details`
--

INSERT INTO `tbl_order_details` (`order_id`, `product_id`, `product_quantity`, `product_color`, `product_total`) VALUES
(1, 24, 1, 'Brown', 1299),
(1, 3, 1, 'Red', 1199),
(2, 23, 3, 'Black', 3897);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_products`
--

DROP TABLE IF EXISTS `tbl_products`;
CREATE TABLE IF NOT EXISTS `tbl_products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `thumbnail` tinytext NOT NULL,
  `category` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `categories_category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_products`
--

INSERT INTO `tbl_products` (`id`, `name`, `description`, `thumbnail`, `category`) VALUES
(1, 'Relaxed Fit Jersey top T-shirt', 'Top in soft cotton jersey with a Relaxed fit with long sleeves.', 'images/Relax1.jpeg', 1),
(2, 'Regular Fit Jersey top T-shirt', 'Regular-fit top in soft cotton jersey with round neckline and long sleeves.', 'images/relaxp1.jpeg', 1),
(3, 'Relaxed Fit Full sleeve T-shirt', 'Slim-fit polo shirt in soft cotton jersey,', 'images/a1.jpeg', 1),
(4, 'Regular Fit Full sleeve T-shirt', 'Polo shirt in soft, fine-knit cotton.', 'images/e1.jpeg', 1),
(5, 'Relaxed Fit Hoodie', 'Relaxed fit Hoodie in sweatshirt fabric made from a cotton blend.', 'images/c1.jpeg', 6),
(6, 'Oversized Fit hoodie', 'Oversized hoodie in sweatshirt fabric made from a cotton blend.', 'images/d1.jpeg', 6),
(7, 'Regular Fit Hoodie', 'Relaxed fit Sweatshirt with dropped shoulders.', 'images/g1.jpeg', 6),
(8, 'Loose Fit Sweatshirt', 'Loose fit Sweatshirt with dropped shoulders.', 'images/loosefit-sweatshirt.jpeg', 7),
(9, 'Straight Regular Jeans', 'Straight Regular Jeans', 'images/hmgoepprod.jpeg', 5);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_specifications`
--

DROP TABLE IF EXISTS `tbl_specifications`;
CREATE TABLE IF NOT EXISTS `tbl_specifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `size` varchar(30) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `pid` int(11) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_specifications`
--

INSERT INTO `tbl_specifications` (`id`, `size`, `quantity`, `price`, `pid`, `date`) VALUES
(1, 'S', 10, 899, 1, '2023-12-30 07:43:42'),
(2, 'M', 10, 999, 1, '2023-12-31 09:46:31'),
(3, 'L', 9, 1199, 1, '2023-12-31 09:46:53'),
(4, 'XL', 10, 1299, 1, '2023-12-31 09:47:19'),
(5, 'XXL', 10, 1599, 1, '2023-12-31 09:47:36'),
(6, 'S', 10, 1499, 5, '2023-12-31 09:47:50'),
(7, 'M', 10, 1499, 5, '2024-01-03 06:57:31'),
(8, 'L', 10, 1599, 5, '2024-01-11 11:45:34'),
(9, 'XL', 10, 1699, 5, '2024-01-11 23:02:05'),
(10, 'XXL', 10, 1999, 5, '2024-01-11 23:02:15'),
(11, 'S', 10, 999, 2, '2024-01-11 23:02:47'),
(12, 'M', 10, 699, 2, '2024-01-24 08:37:53'),
(13, 'L', 8, 699, 2, '2024-01-24 08:39:09'),
(14, 'XL', 10, 699, 2, '2024-01-24 08:39:17'),
(15, 'XXL', 10, 699, 2, '2024-01-24 08:39:25'),
(16, 'S', 10, 1500, 3, '2024-01-24 08:39:49'),
(17, 'M', 10, 1500, 3, '2024-01-24 08:39:59'),
(18, 'XXL', 10, 1500, 3, '2024-01-24 08:40:16'),
(19, 'S', 10, 899, 4, '2024-01-24 08:40:45'),
(20, 'M', 10, 899, 4, '2024-01-24 08:40:57'),
(21, 'XL', 10, 899, 4, '2024-01-24 08:41:08'),
(22, 'XXL', 10, 899, 4, '2024-01-24 08:41:23'),
(23, 'S', 7, 1299, 7, '2024-01-24 08:41:37'),
(24, 'L', 9, 1299, 7, '2024-01-24 08:41:50'),
(25, 'XL', 10, 1299, 7, '2024-01-24 08:42:05'),
(26, 'XXL', 10, 1299, 7, '2024-01-24 08:42:18'),
(27, 'S', 10, 1199, 6, '2024-01-24 08:42:40'),
(28, 'M', 10, 1299, 6, '2024-01-24 08:42:52'),
(29, 'L', 10, 1399, 6, '2024-01-24 08:43:06'),
(30, '32', 10, 1799, 9, '2024-02-16 09:30:20'),
(31, '34', 10, 1899, 9, '2024-02-16 09:30:20');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users`
--

DROP TABLE IF EXISTS `tbl_users`;
CREATE TABLE IF NOT EXISTS `tbl_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` tinytext NOT NULL,
  `secret` tinytext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_users`
--

INSERT INTO `tbl_users` (`id`, `fname`, `lname`, `email`, `secret`) VALUES
(1, 'john', 'patil', 'john@gmail.com', '$2b$12$.3e9yMxmMO4ECtzsOetx2OSEhuI2lVdy7bfZ4pe/ZnWzCJNWFFGh.'),
(2, 'onkar', 'savaratkar', 'onkar@gmail.com', '$2b$12$YvMzUvm2YoQcQuHSgLkfVuryEcPDrirgjk8na5nIBOdWCpni1.xAK'),
(3, 'rajdeep', 'jadhav', 'rajdeep@gmail.com', '$2b$12$TcN6.WgJDe4lJbiZSIYsSuCscb4cqNN3W9GchiDTLupu9Rx5qZjG.'),
(4, 'Sam', 'patil', 'sam@gmail.com', '$2b$12$XHnY74Trow7NjmPCNupgGuUkP02x3akfUYyREQ16MHAWXhQMCSWwK');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_addresses`
--
ALTER TABLE `tbl_addresses`
  ADD CONSTRAINT `tbl_addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`);

--
-- Constraints for table `tbl_cart`
--
ALTER TABLE `tbl_cart`
  ADD CONSTRAINT `tbl_cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`);

--
-- Constraints for table `tbl_orders`
--
ALTER TABLE `tbl_orders`
  ADD CONSTRAINT `tbl_orders_ibfk_1` FOREIGN KEY (`order_user`) REFERENCES `tbl_users` (`id`),
  ADD CONSTRAINT `tbl_orders_ibfk_2` FOREIGN KEY (`order_shipto`) REFERENCES `tbl_addresses` (`id`);

--
-- Constraints for table `tbl_order_details`
--
ALTER TABLE `tbl_order_details`
  ADD CONSTRAINT `tbl_order_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `tbl_orders` (`order_id`),
  ADD CONSTRAINT `tbl_order_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `tbl_specifications` (`id`);

--
-- Constraints for table `tbl_products`
--
ALTER TABLE `tbl_products`
  ADD CONSTRAINT `categories_category` FOREIGN KEY (`category`) REFERENCES `tbl_categories` (`id`);

--
-- Constraints for table `tbl_specifications`
--
ALTER TABLE `tbl_specifications`
  ADD CONSTRAINT `tbl_specifications_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `tbl_products` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
