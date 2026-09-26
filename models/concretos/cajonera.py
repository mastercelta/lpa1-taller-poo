from ..categorias.almacenamiento import Almacenamiento


class Cajonera(Almacenamiento):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 num_cajones: int = 3, tiene_ruedas: bool = False):
        super().__init__(nombre, material, color, precio_base, num_cajones=num_cajones)
        self._tiene_ruedas = tiene_ruedas

    @property
    def tiene_ruedas(self) -> bool:
        return self._tiene_ruedas

    @tiene_ruedas.setter
    def tiene_ruedas(self, value: bool) -> None:
        self._tiene_ruedas = value

    def calcular_precio(self) -> float:
        precio = self.precio_base
        precio *= self.calcular_factor_capacidad()

        if self.tiene_ruedas:
            precio += 30.0

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        descripcion = f"{self} - {self.obtener_info_almacenamiento()}"
        if self.tiene_ruedas:
            descripcion += ", con ruedas"
        return descripcion
