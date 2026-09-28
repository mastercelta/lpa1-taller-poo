from abc import ABC, abstractmethod
from ..mueble import Mueble


class Almacenamiento(Mueble):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 num_cajones: int, capacidad_volumen: float = 0.0):
        super().__init__(nombre, material, color, precio_base)
        self._num_cajones = num_cajones
        self._capacidad_volumen = capacidad_volumen

    @property
    def num_cajones(self) -> int:
        return self._num_cajones

    @property
    def capacidad_volumen(self) -> float:
        return self._capacidad_volumen

    @num_cajones.setter
    def num_cajones(self, value: int) -> None:
        if value < 0:
            raise ValueError("El número de cajones no puede ser negativo")
        self._num_cajones = value

    @capacidad_volumen.setter
    def capacidad_volumen(self, value: float) -> None:
        if value < 0:
            raise ValueError("La capacidad de volumen no puede ser negativa")
        self._capacidad_volumen = value

    def calcular_factor_capacidad(self) -> float:
        factor = 1.0
        factor += self.num_cajones * 0.05
        return factor

    def obtener_info_almacenamiento(self) -> str:
        info = f"Cajones: {self.num_cajones}"
        if self.capacidad_volumen:
            info += f", Capacidad: {self.capacidad_volumen}L"
        return info

    @abstractmethod
    def calcular_precio(self) -> float:
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        pass
