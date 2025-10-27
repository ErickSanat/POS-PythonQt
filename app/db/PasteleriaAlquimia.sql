-- Active: 1760498661977@@127.0.0.1@5432@pasteleria_alquimia
CREATE DATABASE pasteleria_alquimia;
\c pasteleria_alquimia;

-- TABLA ROLES
CREATE TABLE rol (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL CHECK (nombre IN ('admin','empleado'))
);

-- TABLA USUARIOS
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL CHECK (usuario ~ '^[a-zA-Z0-9_]+$'),
    contrasena VARCHAR(255) NOT NULL CHECK (LENGTH(contrasena) >= 8),
    id_rol INT REFERENCES rol(id_rol) ON DELETE SET NULL
);

-- TABLA EMPLEADOS
CREATE TABLE empleado (
    id_empleado SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL CHECK (nombre ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'),
    direccion TEXT NOT NULL CHECK (LENGTH(TRIM(direccion)) > 0),
    telefono BIGINT NOT NULL CHECK (telefono > 0),
    id_usuario INT UNIQUE REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

-- TABLA CLIENTES
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL CHECK (nombre ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$' AND LENGTH(TRIM(nombre)) > 0),
    telefono BIGINT CHECK (telefono IS NULL OR telefono > 0),
    correo VARCHAR(100) CHECK (correo IS NULL OR correo ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- TABLA CATEGORÍAS
CREATE TABLE categoria (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE CHECK (nombre ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s]+$' AND LENGTH(TRIM(nombre)) > 0),
    descripcion TEXT
);

-- TABLA PRODUCTOS
CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL CHECK (LENGTH(TRIM(nombre)) > 0),
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    imagen VARCHAR(100) DEFAULT NULL,
    id_categoria INT REFERENCES categoria(id_categoria) ON DELETE SET NULL
);

-- TABLA RECETAS
CREATE TABLE receta (
    id_receta SERIAL PRIMARY KEY,
    id_producto INT UNIQUE REFERENCES producto(id_producto) ON DELETE CASCADE,
    descripcion TEXT,
    instrucciones TEXT NOT NULL CHECK (LENGTH(TRIM(instrucciones)) > 0)
);

-- TABLA PROVEEDORES
CREATE TABLE proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL CHECK (nombre ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s]+$' AND LENGTH(TRIM(nombre)) > 0),
    nombre_contacto VARCHAR(100) CHECK (nombre_contacto IS NULL OR nombre_contacto ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'),
    telefono BIGINT NOT NULL CHECK (telefono > 0),
    direccion TEXT CHECK (direccion IS NULL OR LENGTH(TRIM(direccion)) > 0),
    activo BOOLEAN DEFAULT TRUE
);

-- TABLA PROMOCIONES
CREATE TABLE promocion (
    id_promocion SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    porcentaje INT NOT NULL,
    descripcion TEXT
);

-- TABLA TIPOS DE PAGO
CREATE TABLE tipo_pago (
    id_tipo_pago SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL CHECK (nombre IN ('efectivo','transferencia','tarjeta'))
);

-- TABLA PAGOS
CREATE TABLE pago (
    id_pago SERIAL PRIMARY KEY,
    id_tipo_pago INT REFERENCES tipo_pago(id_tipo_pago) ON DELETE SET NULL,
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad >= 0)
);

-- TABLA VENTAS
CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_empleado INT REFERENCES empleado(id_empleado) ON DELETE SET NULL,
    id_cliente INT REFERENCES cliente(id_cliente) ON DELETE SET NULL,
    id_promocion INT REFERENCES promocion(id_promocion) ON DELETE SET NULL,
    id_pago INT REFERENCES pago(id_pago) ON DELETE SET NULL,
    total NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (total >= 0)
);

-- TABLA DETALLE DE VENTA
CREATE TABLE detalle_venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INT REFERENCES venta(id_venta) ON DELETE CASCADE,
    id_producto INT REFERENCES producto(id_producto) ON DELETE SET NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    subtotal NUMERIC(10,2) NOT NULL CHECK (subtotal >= 0)
);

-- TABLA CAJAS
CREATE TABLE caja (
    id_caja SERIAL PRIMARY KEY,
    fecha_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre TIMESTAMP,
    monto_inicial NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (monto_inicial >= 0),
    monto_final NUMERIC(10,2) CHECK (monto_final IS NULL OR monto_final >= 0),
    estado VARCHAR(20) DEFAULT 'abierta' CHECK (estado IN ('abierta','cerrada')),
    id_empleado INT REFERENCES empleado(id_empleado) ON DELETE SET NULL,
    CHECK (fecha_cierre IS NULL OR fecha_cierre >= fecha_apertura)
);

INSERT INTO rol (nombre) VALUES ('admin'), ('empleado');
INSERT INTO tipo_pago (nombre) VALUES ('Efectivo'), ('Tarjeta'), ('Transferencia');