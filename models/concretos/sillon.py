from ..categorias.asientos import Asiento


class Sillon(Asiento):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 tiene_respaldo: bool = True, material_tapizado: str = None,
                 es_reclinable: bool = False, tiene_reposapiés: bool = False):
        super().__init__(nombre, material, color, precio_base,
                          capacidad_personas=1, tiene_respaldo=tiene_respaldo,
                          material_tapizado=material_tapizado)
        self._es_reclinable = es_reclinable
        self._tiene_reposapiés = tiene_reposapiés

    @property
    def es_reclinable(self) -> bool:
        return self._es_reclinable

    @es_reclinable.setter
    def es_reclinable(self, value: bool) -> None:
        self._es_reclinable = value

    @property
    def tiene_reposapiés(self) -> bool:
        return self._tiene_reposapiés

    @tiene_reposapiés.setter
    def tiene_reposapiés(self, value: bool) -> None:
        self._tiene_reposapiés = value

    def calcular_precio(self) -> float:
        precio = self.precio_base
        precio *= self.calcular_factor_comodidad()

        if self.es_reclinable:
            precio += 100.0
        if self.tiene_reposapiés:
            precio += 50.0

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        descripcion = f"{self} - {self.obtener_info_asiento()}"
        if self.es_reclinable:
            descripcion += ", reclinable"
        if self.tiene_reposapiés:
            descripcion += ", con reposapiés"
        return descripcion
