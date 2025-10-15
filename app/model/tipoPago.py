class TipoPago:
    def __init__(
        self,
        id_tipo_pago: int=None,
        nombre: str=None
    ):
        self.id_tipo_pago = id_tipo_pago
        self.nombre = nombre
    
    def __repr__(self):
        return f"""
    id_tipo_pago: {self.id_tipo_pago}
    nombre: {self.nombre}
"""