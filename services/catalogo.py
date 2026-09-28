from typing import List, Optional
from models.mueble import Mueble


class Catalogo:

    def __init__(self, muebles: Optional[List[Mueble]] = None):
        self._muebles = muebles if muebles is not None else []

    @property
    def muebles(self) -> List[Mueble]:
        return self._muebles.copy()

    def __len__(self) -> int:
        return len(self._muebles)

    def buscar_por_nombre(self, nombre: str) -> List[Mueble]:
        if not nombre or not nombre.strip():
            return []

        nombre_lower = nombre.lower().strip()
        return [m for m in self._muebles if nombre_lower in m.nombre.lower()]
