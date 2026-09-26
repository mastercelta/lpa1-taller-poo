from abc import ABC, abstractmethod
from ..mueble import Mueble


class Superficie(Mueble):

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 forma: str, resistencia_peso: float = 0.0):
        super().__init__(nombre, material, color, precio_base)
        self._forma = forma
        self._resistencia_peso = resistencia_peso

    @property
    def forma(self) -> str:
        return self._forma

    @property
    def resistencia_peso(self) -> float:
        return self._resistencia_peso

    @forma.setter
    def forma(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("La forma no puede estar vacía")
        self._forma = value.strip()

    @resistencia_peso.setter
    def resistencia_peso(self, value: float) -> None:
        if value < 0:
            raise ValueError("La resistencia de peso no puede ser negativa")
        self._resistencia_peso = value

    def calcular_factor_estabilidad(self) -> float:
        factor = 1.0
        if self.forma.lower() == "redonda":
            factor += 0.05
        if self.resistencia_peso:
            factor += min(self.resistencia_peso / 100, 0.3)
        return factor

    def obtener_info_superficie(self) -> str:
        info = f"Forma: {self.forma}"
        if self.resistencia_peso:
            info += f", Resistencia: {self.resistencia_peso}kg"
        return info

    @abstractmethod
    def calcular_precio(self) -> float:
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        pass
