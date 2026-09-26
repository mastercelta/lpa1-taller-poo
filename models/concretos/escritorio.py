from ..categorias.superficies import Superficie


class Escritorio(Superficie):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 forma: str, tiene_cajones: bool = False, num_cajones: int = 0,
                 tiene_iluminacion: bool = False):
        super().__init__(nombre, material, color, precio_base, forma=forma)
        self._tiene_cajones = tiene_cajones
        self._num_cajones = num_cajones
        self._tiene_iluminacion = tiene_iluminacion

    @property
    def tiene_cajones(self) -> bool:
        return self._tiene_cajones

    @tiene_cajones.setter
    def tiene_cajones(self, value: bool) -> None:
        self._tiene_cajones = value

    @property
    def num_cajones(self) -> int:
        return self._num_cajones

    @num_cajones.setter
    def num_cajones(self, value: int) -> None:
        if value < 0:
            raise ValueError("El número de cajones no puede ser negativo")
        self._num_cajones = value

    @property
    def tiene_iluminacion(self) -> bool:
        return self._tiene_iluminacion

    @tiene_iluminacion.setter
    def tiene_iluminacion(self, value: bool) -> None:
        self._tiene_iluminacion = value

    def calcular_precio(self) -> float:
        precio = self.precio_base
        precio *= self.calcular_factor_estabilidad()

        if self.tiene_cajones:
            precio += self.num_cajones * 25.0
        if self.tiene_iluminacion:
            precio += 60.0

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        descripcion = f"{self} - {self.obtener_info_superficie()}"
        if self.tiene_cajones:
            descripcion += f", {self.num_cajones} cajones"
        if self.tiene_iluminacion:
            descripcion += ", con iluminación"
        return descripcion
