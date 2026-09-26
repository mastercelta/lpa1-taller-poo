from ..categorias.asientos import Asiento


class Sofa(Asiento):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 capacidad_personas: int = 2, tiene_respaldo: bool = True,
                 material_tapizado: str = None, es_modular: bool = False,
                 incluye_cojines: bool = False):
        super().__init__(nombre, material, color, precio_base,
                          capacidad_personas=capacidad_personas, tiene_respaldo=tiene_respaldo,
                          material_tapizado=material_tapizado)
        self._es_modular = es_modular
        self._incluye_cojines = incluye_cojines

    @property
    def es_modular(self) -> bool:
        return self._es_modular

    @es_modular.setter
    def es_modular(self, value: bool) -> None:
        self._es_modular = value

    @property
    def incluye_cojines(self) -> bool:
        return self._incluye_cojines

    @incluye_cojines.setter
    def incluye_cojines(self, value: bool) -> None:
        self._incluye_cojines = value

    def calcular_precio(self) -> float:
        precio = self.precio_base
        precio *= self.calcular_factor_comodidad()

        if self.es_modular:
            precio += 200.0
        if self.incluye_cojines:
            precio += 50.0

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        descripcion = f"{self} - {self.obtener_info_asiento()}"
        if self.es_modular:
            descripcion += ", modular"
        if self.incluye_cojines:
            descripcion += ", incluye cojines"
        return descripcion
