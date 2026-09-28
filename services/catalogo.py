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

    def filtrar_por_precio(self, precio_min: float, precio_max: float) -> List[Mueble]:
        if precio_min < 0:
            precio_min = 0

        resultados = []
        for mueble in self._muebles:
            try:
                if precio_min <= mueble.calcular_precio() <= precio_max:
                    resultados.append(mueble)
            except Exception:
                continue

        return resultados

    def filtrar_por_material(self, material: str) -> List[Mueble]:
        if not material or not material.strip():
            return []

        material_lower = material.lower().strip()
        return [m for m in self._muebles if m.material.lower() == material_lower]

    def filtrar_por_tipo(self, tipo_clase: type) -> List[Mueble]:
        return [m for m in self._muebles if isinstance(m, tipo_clase)]

    def ordenar_por_precio(self, descendente: bool = False) -> List[Mueble]:
        def precio_seguro(mueble: Mueble) -> float:
            try:
                return mueble.calcular_precio()
            except Exception:
                return float("inf")

        return sorted(self._muebles, key=precio_seguro, reverse=descendente)
