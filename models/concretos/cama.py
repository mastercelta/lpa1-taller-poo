from ..mueble import Mueble


class Cama(Mueble):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 tamaño: str = "matrimonial", incluye_colchon: bool = False,
                 tiene_cabecera: bool = False):
        super().__init__(nombre, material, color, precio_base)
        self._tamaño = tamaño
        self._incluye_colchon = incluye_colchon
        self._tiene_cabecera = tiene_cabecera

    @property
    def tamaño(self) -> str:
        return self._tamaño

    @tamaño.setter
    def tamaño(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El tamaño no puede estar vacío")
        self._tamaño = value.strip()

    @property
    def incluye_colchon(self) -> bool:
        return self._incluye_colchon

    @incluye_colchon.setter
    def incluye_colchon(self, value: bool) -> None:
        self._incluye_colchon = value

    @property
    def tiene_cabecera(self) -> bool:
        return self._tiene_cabecera

    @tiene_cabecera.setter
    def tiene_cabecera(self, value: bool) -> None:
        self._tiene_cabecera = value

    def calcular_precio(self) -> float:
        precio = self.precio_base

        factores_tamaño = {"individual": 1.0, "matrimonial": 1.3, "queen": 1.5, "king": 1.8}
        precio *= factores_tamaño.get(self.tamaño.lower(), 1.0)

        if self.incluye_colchon:
            precio += 300.0
        if self.tiene_cabecera:
            precio += 100.0

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        descripcion = f"{self} - Tamaño: {self.tamaño}"
        if self.incluye_colchon:
            descripcion += ", incluye colchón"
        if self.tiene_cabecera:
            descripcion += ", con cabecera"
        return descripcion
