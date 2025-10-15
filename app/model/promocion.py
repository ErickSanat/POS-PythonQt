DIAS = [
    'Lunes',
    'Martes',
    'Miércoles',
    'Jueves',
    'Viernes',
    'Sábado',
    'Domingo'
]
class Promocion:
    def __init__(
        self,
        id_promocion: int=None,
        dia_semana: str=None, 
        # checar si se puede meter enum
        descripción: str=None
    ):
        self.id_promocion = id_promocion
        self.dia_semana = dia_semana
        self.descripción = descripción