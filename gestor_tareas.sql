-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-05-2024 a las 20:45:11
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestor_tareas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id_Tareas` int(3) NOT NULL,
  `Nombre` varchar(200) NOT NULL,
  `Fecha_Inicio` datetime DEFAULT NULL,
  `Fecha_final` datetime DEFAULT NULL,
  `Estado` varchar(200) DEFAULT NULL,
  `usuario` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `Id_Usuarios` int(3) NOT NULL,
  `Nombre_usuario` varchar(200) NOT NULL,
  `Apellidos_usuario` varchar(200) NOT NULL,
  `Genero` varchar(9) NOT NULL,
  `Email_usuario` varchar(200) NOT NULL,
  `Usuario_name` varchar(200) NOT NULL,
  `Contrasena_Usuario` varchar(200) NOT NULL,
  `Rol` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`Id_Usuarios`, `Nombre_usuario`, `Apellidos_usuario`, `Genero`, `Email_usuario`, `Usuario_name`, `Contrasena_Usuario`, `Rol`) VALUES
(9, 'Sofia', 'Garcia', 'Femenino', 'garcia@gmail.com', 'garcia2024', 'scrypt:32768:8:1$7RXv3GDSmfIa0nve$b5ce1cad4ff502d72335492dfc93ebc6f3e9cec67ceb1383972edb7b1785a5f94af86476b7a5422a6f349441564df5f48c98410c268a70a6a98fcc4018783665', 'Administrador'),
(10, 'Karen', 'Martinez', 'Femenino', 'masilka.km@gmail.com', 'martinez2024', 'scrypt:32768:8:1$paVmX2fVg2SF1Pn7$2c761d8e96d4017a1793b71075e84aa2abe67cf56759eb83910b8ee8d4f495f96e87b32ab8241113d55a8e8c85d816449089efe826a90ea15edb9a4c9e2b55a0', 'Administrador'),
(11, 'Elias', 'alvarez', 'Masculino', 'Elias@gmail.com', 'Tonto', 'scrypt:32768:8:1$WPxagd7gAmjDQsC8$092cc226ab0e2c38afabb0875584b03554791fa4e1c4c225745eab0f37fadd835b3a249b32b19fff86f74ddc53a62dd66b06598796f96d7993e8c2687afeb5b0', 'Usuario'),
(14, 'Astrid', 'Silva', 'Femenino', 'asilcy75@gmail.com', 'madre', 'scrypt:32768:8:1$mLIaikBwIUVu63lS$e2f5950cf1ac96295739db19d55564b9e735671dd1ec201d69f0021288913bb8d0521bd496193c4af3b03b4538371fd348979a61c6f6817b94a994141835c5f0', 'Usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_Tareas`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`Id_Usuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_Tareas` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `Id_Usuarios` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
