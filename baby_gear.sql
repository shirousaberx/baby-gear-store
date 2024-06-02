-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 08, 2024 at 03:25 PM
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
-- Database: `uas_python`
--

-- --------------------------------------------------------

--
-- Table structure for table `produk`
--

CREATE TABLE `produk` (
  `id` int(10) NOT NULL,
  `nama` text NOT NULL,
  `deskripsi` longtext NOT NULL,
  `sewa_per_bulan` int(100) NOT NULL,
  `image` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `produk`
--

INSERT INTO `produk` (`id`, `nama`, `deskripsi`, `sewa_per_bulan`, `image`) VALUES
(7, 'Gendongan Bayi', 'Direkomendasikan untuk usia bayi 5 bulan ke atas hingga berat badan bayi maksimal 12 kg', 50000, '1698492329619_gendongan_bayi.jpeg'),
(8, 'Tissue Bayi', 'untuk membersihkan bagian tubuh bayi saat mengganti popok, membersihkan tubuh dari keringat dan kotoran', 10000, '1698492878187_tissue_bayi.jpg'),
(9, 'Stroller', 'Bayi usia 2 bulan boleh pakai stroller atau kereta bayi', 150000, '1698493053334_stroller.jpg'),
(12, 'Ayunan Bayi', 'Ayunan bayi ini cocok untuk bayi usia dibawah 1 tahun karena dapat memberikan kenyamanan dan keamanan pada bayi.', 40000, '1698511966600_ayunan_bayi.jpeg'),
(13, 'Baby Walker', 'Baby Walker biasa digunakan untuk anak usia 6-12 bulan yang sedang belajar berjalan, biasanya digunakan oleh bayi yang sudah bisa duduk dengan stabil ', 50000, '1698512098120_babywalker.jpeg'),
(14, 'Bak Mandi Bayi', 'digunakan untuk memandikan bayi dengan nyaman karena adanya sandaran sehingga bayi dapat mandi dengan nyaman ', 20000, '1698512182559_bak_mandi_bayi.jpg'),
(15, 'Baju Bayi', 'pakaian bayi yang nyaman untuk digunakan dan hangat untuk bayi dengan bahan yang tidak membahayakan kulit bayi', 30000, '1698512382482_baju_bayi.jpeg'),
(16, 'Botol Susu Bayi', 'botol yang digunakan untuk meminum ketika bayi sudah bisa lepas dari ASI yang memiliki pegangan di botolnya sehingga tidak mudah terlepas dari genggaman bayi ', 40000, '1698512808808_botol_susu.jpeg'),
(17, 'Bouncer Bayi', 'Bouncer bayi cocok digunakan untuk bayi berusia antara 0-6 bulan, Pada usia ini, bayi masih belum dapat duduk sendiri dengan stabil. Bouncer memberikan lingkungan yang nyaman dan aman bagi bayi untuk duduk atau berbaring sambil mengamati sekitarnya atau merespon rangsangan ', 100000, '1698513089335_bouncer_bayi.jpeg'),
(18, 'Box Bayi', 'tempat tidur kecil yang dirancang khusus untuk bayi. Fungsi utama dari box bayi adalah memberikan tempat yang aman, nyaman, dan bebas risiko untuk bayi tidur atau beristirahat.', 200000, '1698513175524_box_bayi.jpg'),
(19, 'Kursi Makan Bayi', 'Kursi makan bayi dirancang khusus untuk menyediakan tempat yang aman dan nyaman bagi bayi atau anak kecil untuk makan.', 150000, '1698513318858_kursi_makan_bayi.png'),
(20, 'Car Seat Bayi', 'Car seat bayi adalah perangkat keselamatan khusus yang dirancang untuk mengamankan bayi atau anak kecil selama perjalanan menggunakan kendaraan', 200000, '1698513396847_car_seat_bayi.jpeg'),
(21, 'Gunting Kuku Bayi ', 'Gunting kuku bayi biasanya digunakan untuk memotong kuku bayi yang masih sangat lembut dan halus. Namun, memotong kuku bayi bukanlah praktik yang umum dilakukan pada bayi yang sangat muda, terutama pada bayi baru lahir', 10000, '1698513493270_gunting_kuku_bayi.jpg'),
(22, 'Handuk Bayi', 'Handuk bayi dapat digunakan sejak bayi baru lahir. Handuk bayi dirancang khusus untuk kulit yang lembut dan sensitif bayi, dan mereka biasanya terbuat dari bahan yang lembut dan menyerap air dengan baik', 10000, '1698513763090_handuk_bayi.jpg'),
(23, 'Mainan Bayi', 'Mainan bayi dapat digunakan sejak bayi baru lahir hingga masa perkembangannya sebagai anak balita', 25000, '1698513868888_mainan_bayi.jpg'),
(24, 'Minyak Bayi ', 'Minyak bayi dapat digunakan untuk bayi sejak mereka baru lahir. Minyak bayi umumnya digunakan untuk berbagai tujuan perawatan kulit bayi.', 15000, '1698514204840_minyak_bayi.jpg'),
(25, 'Peralatan Makan Bayi ', 'Peralatan makan bayi dapat digunakan sejak bayi mulai memasuki fase pemberian makanan padat, biasanya sekitar usia 4 hingga 6 bulan. Namun, waktu mulai memberikan makanan padat kepada bayi sebaiknya disesuaikan dengan perkembangan individu bayi dan konsultasi dengan dokter anak.', 20000, '1698514285210_peralatan_makan.jpeg'),
(26, 'Sterilizer Bayi', 'Sterilizer bayi digunakan untuk membersihkan dan membunuh kuman pada peralatan bayi seperti botol susu, dot, dan pompa ASI. Tujuan utama dari menggunakan sterilizer bayi adalah untuk menjaga kebersihan dan keamanan peralatan yang digunakan oleh bayi, terutama yang terkait dengan makanan dan minuman.', 100000, '1698514382967_Sterilizer_bayi.jpeg'),
(27, 'Termometer Bayi', 'Termometer bayi digunakan untuk mengukur suhu tubuh bayi. Pemantauan suhu tubuh bayi penting karena suhu tubuh yang tidak normal dapat menjadi tanda adanya penyakit atau infeksi', 50000, '1698514534090_termometer_bayi.jpg'),
(28, 'Tas Bayi ', 'Tas bayi memiliki berbagai kegunaan dan fungsinya yang memudahkan orang tua dalam merawat dan membawa perlengkapan bayi', 100000, '1698514613039_tas_bayi.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `sewa`
--

CREATE TABLE `sewa` (
  `id` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_produk` int(11) NOT NULL,
  `tanggal_sewa` date NOT NULL,
  `lama_sewa` int(11) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `dikembalikan` char(1) NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sewa`
--

INSERT INTO `sewa` (`id`, `id_user`, `id_produk`, `tanggal_sewa`, `lama_sewa`, `jumlah`, `dikembalikan`) VALUES
(5, 9, 20, '2023-12-15', 3, 2, 'Y'),
(6, 9, 8, '2023-12-15', 1, 1, 'Y'),
(7, 9, 22, '2023-12-15', 2, 2, 'Y'),
(8, 9, 13, '2023-12-15', 1, 1, 'Y'),
(9, 9, 17, '2023-12-15', 1, 2, 'Y'),
(10, 9, 14, '2024-01-08', 3, 2, 'Y'),
(13, 9, 7, '2024-01-08', 1, 1, 'Y'),
(14, 9, 19, '2024-01-08', 2, 2, 'N'),
(17, 12, 8, '2024-01-08', 1, 1, 'Y'),
(18, 12, 9, '2024-01-08', 2, 2, 'N'),
(19, 12, 12, '2024-01-08', 3, 3, 'Y'),
(20, 12, 13, '2024-01-08', 4, 4, 'N');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `tgl_lahir` date DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `hobi` varchar(30) DEFAULT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `nama`, `email`, `password`, `tgl_lahir`, `alamat`, `gender`, `hobi`, `role`) VALUES
(6, 'admin', 'admin@gmail.com', 'admin', '2023-10-01', 'Jl. ABC No. 3', 'Pria', 'Membaca', 'Administrator'),
(9, 'Useredited', 'user@gmail.com', 'user', '2023-12-13', 'abcde', 'Pria', 'Membaca, Menulis', 'User'),
(10, 'admin2', 'admin2@gmail.com', 'admin2', '2023-12-26', 'abcd', 'Pria', 'Membaca', 'Administrator'),
(12, 'user2', 'user2@gmail.com', 'user2', '2024-02-01', '', 'Wanita', 'Membaca', 'User');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `produk`
--
ALTER TABLE `produk`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sewa`
--
ALTER TABLE `sewa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_id_user` (`id_user`),
  ADD KEY `fk_id_produk` (`id_produk`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `produk`
--
ALTER TABLE `produk`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `sewa`
--
ALTER TABLE `sewa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sewa`
--
ALTER TABLE `sewa`
  ADD CONSTRAINT `fk_id_produk` FOREIGN KEY (`id_produk`) REFERENCES `produk` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_id_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

DELIMITER $$
--
-- Events
--
CREATE DEFINER=`root`@`localhost` EVENT `expire_sewa` ON SCHEDULE EVERY 5 SECOND STARTS '2023-12-15 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
	UPDATE sewa
    SET dikembalikan = "Y"
    WHERE ADDDATE(tanggal_sewa, INTERVAL lama_sewa MONTH) < CURRENT_DATE();
END$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
