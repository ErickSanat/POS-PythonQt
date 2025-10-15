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