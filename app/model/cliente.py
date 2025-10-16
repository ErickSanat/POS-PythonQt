class Cliente:
    def __init__(
        self,
        id_cliente: int=None,
        nombre: str=None,
        telefono: int=None,
        correo: str=None
    ):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
    
    def __repr__(self):
        from json import dumps
        return dumps(
            {
                "id_cliente": self.id_cliente,
                "nombre": self.nombre,
                "telefono": self.telefono,
                "correo": self.correo
            }, indent=4
        )