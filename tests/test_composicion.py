import pytest
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.composicion.comedor import Comedor


@pytest.fixture
def mesa():
    return Mesa("Mesa Test", "Madera", "Roble", 500.0, "rectangular", 4)


@pytest.fixture
def comedor(mesa):
    return Comedor("Comedor Test", mesa)


def crear_silla(nombre="Silla"):
    return Silla(nombre, "Madera", "Roble", 100.0, True)


class TestCreacionComedor:

    def test_comedor_vacio(self, comedor, mesa):
        assert comedor.nombre == "Comedor Test"
        assert comedor.mesa is mesa
        assert comedor.sillas == []
        assert len(comedor) == 1

    def test_comedor_con_sillas_iniciales(self, mesa):
        sillas = [crear_silla("S1"), crear_silla("S2")]
        comedor = Comedor("Con Sillas", mesa, sillas)
        assert len(comedor.sillas) == 2
        assert len(comedor) == 3

    def test_sillas_retorna_copia(self, comedor):
        comedor.agregar_silla(crear_silla())
        copia = comedor.sillas
        copia.clear()
        assert len(comedor.sillas) == 1


class TestAgregarQuitarSillas:

    def test_agregar_silla_valida(self, comedor):
        resultado = comedor.agregar_silla(crear_silla("Nueva"))
        assert "exitosamente" in resultado.lower()
        assert len(comedor.sillas) == 1

    def test_agregar_objeto_no_silla(self, comedor, mesa):
        resultado = comedor.agregar_silla(mesa)
        assert "error" in resultado.lower()
        assert len(comedor.sillas) == 0

    def test_agregar_silla_supera_capacidad(self, comedor):
        for i in range(4):
            comedor.agregar_silla(crear_silla(f"S{i}"))
        resultado = comedor.agregar_silla(crear_silla("Extra"))
        assert "capacidad máxima" in resultado.lower()
        assert len(comedor.sillas) == 4

    def test_quitar_silla_valida(self, comedor):
        comedor.agregar_silla(crear_silla("S1"))
        resultado = comedor.quitar_silla(0)
        assert "removida" in resultado.lower()
        assert len(comedor.sillas) == 0

    def test_quitar_silla_sin_sillas(self, comedor):
        resultado = comedor.quitar_silla(0)
        assert "no hay sillas" in resultado.lower()

    def test_quitar_silla_indice_invalido(self, comedor):
        comedor.agregar_silla(crear_silla())
        resultado = comedor.quitar_silla(5)
        assert "inválido" in resultado.lower()
        assert len(comedor.sillas) == 1


class TestPrecios:

    def test_precio_total_solo_mesa(self, comedor, mesa):
        assert comedor.calcular_precio_total() == mesa.calcular_precio()

    def test_precio_total_con_sillas(self, comedor, mesa):
        s1, s2 = crear_silla("S1"), crear_silla("S2")
        comedor.agregar_silla(s1)
        comedor.agregar_silla(s2)
        esperado = mesa.calcular_precio() + s1.calcular_precio() + s2.calcular_precio()
        assert comedor.calcular_precio_total() == round(esperado, 2)

    def test_descuento_con_cuatro_sillas(self, comedor, mesa):
        sillas = [crear_silla(f"S{i}") for i in range(4)]
        for silla in sillas:
            comedor.agregar_silla(silla)
        subtotal = mesa.calcular_precio() + sum(s.calcular_precio() for s in sillas)
        assert comedor.calcular_precio_total() == round(subtotal * 0.95, 2)

    def test_sin_descuento_con_tres_sillas(self, comedor, mesa):
        sillas = [crear_silla(f"S{i}") for i in range(3)]
        for silla in sillas:
            comedor.agregar_silla(silla)
        subtotal = mesa.calcular_precio() + sum(s.calcular_precio() for s in sillas)
        assert comedor.calcular_precio_total() == round(subtotal, 2)


class TestInformacion:

    def test_descripcion_completa_sin_sillas(self, comedor):
        descripcion = comedor.obtener_descripcion_completa()
        assert "COMEDOR TEST" in descripcion
        assert "Ninguna incluida" in descripcion

    def test_descripcion_completa_con_sillas(self, comedor):
        comedor.agregar_silla(crear_silla("S1"))
        descripcion = comedor.obtener_descripcion_completa()
        assert "SILLAS (1 unidades)" in descripcion

    def test_descripcion_menciona_descuento(self, comedor):
        for i in range(4):
            comedor.agregar_silla(crear_silla(f"S{i}"))
        assert "5% de descuento" in comedor.obtener_descripcion_completa()

    def test_resumen(self, comedor, mesa):
        comedor.agregar_silla(crear_silla("S1"))
        resumen = comedor.obtener_resumen()
        assert resumen["nombre"] == "Comedor Test"
        assert resumen["total_muebles"] == 2
        assert resumen["precio_mesa"] == mesa.calcular_precio()
        assert resumen["capacidad_personas"] == 1
        assert "Madera" in resumen["materiales_utilizados"]

    def test_str(self, comedor):
        comedor.agregar_silla(crear_silla())
        assert str(comedor) == "Comedor Comedor Test: Mesa + 1 sillas"

    def test_len(self, comedor):
        assert len(comedor) == 1
        comedor.agregar_silla(crear_silla())
        assert len(comedor) == 2
