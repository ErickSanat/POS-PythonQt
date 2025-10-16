class Proveedor:
    def __init__(
        self,
        id_proveedor: int=None,
        nombre: str=None,
        nombre_contacto: str=None,
        telefono: int=None,
        direccion: str=None,
        activo: bool=None
    ):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.nombre_contacto = nombre_contacto
        self.telefono = telefono
        self.direccion = direccion
        self.activo = activo
    
    def __repr__(self):
        from json import dumps
        return dumps(
            {
                "id_proveedor": self.id_proveedor,
                "nombre": self.nombre,
                "nombre_contacto": self.nombre_contacto,
                "telefono": self.telefono,
                "direccion": self.direccion,
                "activo": self.activo
            }, indent=4
        )