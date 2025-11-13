from .DB import DBConnection
from ..model import Promocion
from ..utils import cerrarConn, cerrarCommit


class PromocionDAO:
    def promociones(self) -> list[Promocion]:
        """Fetch all promotions"""
        promociones: list[Promocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM promocion")
        resultado = cur.fetchall()
        promociones.extend(
            Promocion(
                promocion[0],
                promocion[1],
                promocion[2],
                promocion[3]
            )
            for promocion in resultado
        )
        cerrarConn(cur, conn)
        if promociones:
            return promociones
        else:
            raise TypeError("No existen promociones")
    
    def promocion(self, id_promocion: int) -> Promocion:
        """Fetch a single promotion by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM promocion WHERE id_promocion = %s", (id_promocion,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Promocion(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            return None

    def promocionExistente(self, promocion: Promocion) -> Promocion | bool:
        """Check if promotion exists by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM promocion WHERE nombre = %s", (promocion.nombre,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Promocion(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            return False

    def addPromocion(self, promocion: Promocion):
        """Add a new promotion using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO promocion (nombre, porcentaje, descripcion) VALUES (%s, %s, %s)",
            (promocion.nombre, promocion.porcentaje, promocion.descripcion)
        )
        cerrarCommit(cur, conn)

    def updatePromocion(self, promocion: Promocion):
        """Update a promotion using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE promocion SET nombre=%s, porcentaje=%s, descripcion=%s WHERE id_promocion=%s",
            (promocion.nombre, promocion.porcentaje, promocion.descripcion, promocion.id_promocion)
        )
        cerrarCommit(cur, conn)

    def deletePromocion(self, id_promocion: int):
        """Delete a promotion using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM promocion WHERE id_promocion=%s", (id_promocion,))
        cerrarCommit(cur, conn)

    def buscarPromociones(self, columna: str, aBuscar: str) -> list[Promocion]:
        """Search promotions using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        promociones: list[Promocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['nombre', 'porcentaje', 'descripcion', 'id_promocion']
        if columna not in allowed_columns:
            columna = 'nombre'  # default to safe column
        
        cur.execute(
            f"SELECT * FROM promocion WHERE CAST({columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        promociones.extend(
            Promocion(
                promocion[0],
                promocion[1],
                promocion[2],
                promocion[3]
            )
            for promocion in resultado
        )
        cerrarConn(cur, conn)
        if promociones:
            return promociones
        else:
            raise TypeError("No existen promociones")