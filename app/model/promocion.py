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
        # checar si se puede meter enum
        id_promocion: int=None,
        dia_semana: str=None, 
        descripción: str=None
    ):
        self.id_promocion = id_promocion
        self.dia_semana = dia_semana
        self.descripción = descripción
    
    def __repr__(self):
        return f"""
    id_promocion: {self.id_promocion}
    dia_semana: {self.dia_semana}
    descripción: {self.descripción}
"""