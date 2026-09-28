from ..categorias.almacenamiento import Almacenamiento


class Armario(Almacenamiento):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 num_puertas: int = 2, num_cajones: int = 0, tiene_espejos: bool = False):
        super().__init__(nombre, material, color, precio_base, num_cajones=num_cajones)
        self._num_puertas = num_puertas
        self._tiene_espejos = tiene_espejos

    @property
    def num_puertas(self) -> int:
        return self._num_puertas

    @num_puertas.setter
    def num_puertas(self, value: int) -> None:
        if value < 0:
            raise ValueError("El número de puertas no puede ser negativo")
        self._num_puertas = value

    @property
    def tiene_espejos(self) -> bool:
        return self._tiene_espejos

    @tiene_espejos.setter
    def tiene_espejos(self, value: bool) -> None:
        self._tiene_espejos = value

    def calcular_precio(self) -> float:
        precio = self.precio_base
        precio *= self.calcular_factor_capacidad()
        precio += self.num_puertas * 40.0

        if self.tiene_espejos:
            precio += 80.0

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        descripcion = f"{self} - {self.obtener_info_almacenamiento()}, {self.num_puertas} puertas"
        if self.tiene_espejos:
            descripcion += ", con espejos"
        return descripcion
