CREATE DATABASE PasteleriaAlquimia;

-- Tabla Categorias
CREATE TABLE Categorias (
    categoria_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(255),
    es_para_venta_diaria BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Metodos_Pago
CREATE TABLE Metodos_Pago (
    metodo_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    requiere_terminal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Clientes
CREATE TABLE Clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL CHECK (nombre ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'),
    apellido VARCHAR(100) NOT NULL CHECK (apellido ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'),
    telefono VARCHAR(15) CHECK (telefono ~ '^[0-9+\-\s()]{10,15}$'),
    email VARCHAR(255) CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    direccion TEXT,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    preferencias TEXT,
    alergias TEXT,
    puntos_fidelidad INTEGER DEFAULT 0 CHECK (puntos_fidelidad >= 0),
    fecha_nacimiento DATE CHECK (fecha_nacimiento <= CURRENT_DATE - INTERVAL '1 year'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Empleados
CREATE TABLE Empleados (
    empleado_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL CHECK (nombre ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'),
    apellido VARCHAR(100) NOT NULL CHECK (apellido ~ '^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'),
    puesto VARCHAR(50) NOT NULL CHECK (puesto IN ('vendedor', 'panadero', 'administrador')),
    telefono VARCHAR(15) NOT NULL CHECK (telefono ~ '^[0-9+\-\s()]{10,15}$'),
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    fecha_contratacion DATE NOT NULL CHECK (fecha_contratacion <= CURRENT_DATE),
    salario DECIMAL(10,2) NOT NULL CHECK (salario >= 0),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Usuarios
CREATE TABLE Usuarios (
    usuario_id SERIAL PRIMARY KEY,
    empleado_id INTEGER NOT NULL UNIQUE,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE CHECK (LENGTH(nombre_usuario) >= 4),
    contrasena_hash VARCHAR(255) NOT NULL CHECK (LENGTH(contrasena_hash) >= 60),
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'cajero', 'panadero')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id) ON DELETE CASCADE
);

-- Tabla Cajas
CREATE TABLE Cajas (
    caja_id SERIAL PRIMARY KEY,
    usuario_id_apertura INTEGER NOT NULL,
    usuario_id_cierre INTEGER,
    fecha_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre TIMESTAMP,
    monto_inicial DECIMAL(10,2) NOT NULL CHECK (monto_inicial >= 0),
    monto_final DECIMAL(10,2) CHECK (monto_final >= 0),
    estado VARCHAR(20) DEFAULT 'abierta' CHECK (estado IN ('abierta', 'cerrada')),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id_apertura) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (usuario_id_cierre) REFERENCES Usuarios(usuario_id)
);

-- Tabla Productos
CREATE TABLE Productos (
    producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio_venta DECIMAL(10,2) NOT NULL CHECK (precio_venta >= 0),
    costo_produccion DECIMAL(10,2) CHECK (costo_produccion >= 0),
    codigo_barras VARCHAR(50) UNIQUE,
    categoria_id INTEGER NOT NULL,
    es_percedero BOOLEAN DEFAULT FALSE,
    tiempo_preparacion INTEGER CHECK (tiempo_preparacion >= 0),
    imagen_url VARCHAR(255),
    stock_minimo INTEGER DEFAULT 0 CHECK (stock_minimo >= 0),
    stock_actual INTEGER DEFAULT 0 CHECK (stock_actual >= 0),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id)
);

-- Tabla Ingredientes
CREATE TABLE Ingredientes (
    ingrediente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL CHECK (unidad_medida IN ('gr', 'kg', 'ml', 'l', 'unidades')),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    stock_actual DECIMAL(10,3) DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo DECIMAL(10,3) DEFAULT 0 CHECK (stock_minimo >= 0),
    proveedor_id INTEGER,
    es_alergeno BOOLEAN DEFAULT FALSE,
    tipo_alergeno VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Recetas
CREATE TABLE Recetas (
    receta_id SERIAL PRIMARY KEY,
    producto_id INTEGER NOT NULL,
    ingrediente_id INTEGER NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL CHECK (cantidad > 0),
    instrucciones TEXT,
    version_receta VARCHAR(20) DEFAULT '1.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id) ON DELETE CASCADE,
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(ingrediente_id) ON DELETE CASCADE,
    UNIQUE(producto_id, ingrediente_id, version_receta)
);

-- Tabla Promociones
CREATE TABLE Promociones (
    promocion_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('porcentaje', 'monto_fijo', '2x1', '3x2')),
    valor DECIMAL(10,2) CHECK (valor >= 0),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL CHECK (fecha_fin >= fecha_inicio),
    productos_aplicables JSONB,
    dias_semana VARCHAR(20),
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Ventas
CREATE TABLE Ventas (
    venta_id SERIAL PRIMARY KEY,
    cliente_id INTEGER,
    usuario_id INTEGER NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    descuento DECIMAL(10,2) DEFAULT 0 CHECK (descuento >= 0),
    iva DECIMAL(10,2) NOT NULL CHECK (iva >= 0),
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    metodo_pago_id INTEGER NOT NULL,
    estado VARCHAR(20) DEFAULT 'completada' CHECK (estado IN ('completada', 'cancelada')),
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (metodo_pago_id) REFERENCES Metodos_Pago(metodo_id)
);

-- Tabla Detalles_Venta
CREATE TABLE Detalles_Venta (
    detalle_id SERIAL PRIMARY KEY,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    descuento DECIMAL(10,2) DEFAULT 0 CHECK (descuento >= 0),
    total_linea DECIMAL(10,2) NOT NULL CHECK (total_linea >= 0),
    personalizaciones TEXT,
    es_pedido_especial BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (venta_id) REFERENCES Ventas(venta_id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

-- Tabla Movimientos_Inventario
CREATE TABLE Movimientos_Inventario (
    movimiento_id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('entrada', 'salida', 'ajuste', 'merma')),
    ingrediente_id INTEGER NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INTEGER NOT NULL,
    motivo TEXT,
    costo_total DECIMAL(10,2) CHECK (costo_total >= 0),
    relacion_venta INTEGER,
    relacion_pedido INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(ingrediente_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (relacion_venta) REFERENCES Ventas(venta_id) ON DELETE SET NULL
);

-- ageragar proveedor y comrpa a provedores, tablas
