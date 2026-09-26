from ..categorias.superficies import Superficie


class Mesa(Superficie):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 forma: str, capacidad_personas: int = 4):
        super().__init__(nombre, material, color, precio_base, forma=forma)
        self._capacidad_personas = capacidad_personas

    @property
    def capacidad_personas(self) -> int:
        return self._capacidad_personas

    @capacidad_personas.setter
    def capacidad_personas(self, value: int) -> None:
        if value <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        self._capacidad_personas = value

    def calcular_precio(self) -> float:
        precio = self.precio_base
        precio *= self.calcular_factor_estabilidad()
        precio += self.capacidad_personas * 15.0
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        return f"{self} - {self.obtener_info_superficie()}, capacidad {self.capacidad_personas} personas"
