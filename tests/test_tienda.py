import pytest
from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.sofa import Sofa
from models.composicion.comedor import Comedor


@pytest.fixture
def tienda():
    return TiendaMuebles("Tienda Test")


@pytest.fixture
def tienda_con_inventario(tienda):
    tienda.agregar_mueble(Silla("Silla Clásica", "Madera", "Café", 100.0, True))
    tienda.agregar_mueble(Silla("Silla Metal", "Metal", "Negro", 200.0, True))
    tienda.agregar_mueble(Mesa("Mesa Roble", "Madera", "Roble", 500.0, "rectangular", 4))
    tienda.agregar_mueble(Sofa("Sofá Gris", "Tela", "Gris", 800.0))
    return tienda


class TestInventario:

    def test_tienda_nueva_vacia(self, tienda):
        assert tienda.nombre == "Tienda Test"
        assert tienda.total_muebles == 0

    def test_agregar_mueble_valido(self, tienda):
        resultado = tienda.agregar_mueble(Silla("S", "Madera", "Café", 100.0, True))
        assert "exitosamente" in resultado.lower()
        assert tienda.total_muebles == 1

    def test_agregar_objeto_invalido(self, tienda):
        resultado = tienda.agregar_mueble("no soy un mueble")
        assert "error" in resultado.lower()
        assert tienda.total_muebles == 0

    def test_agregar_comedor_valido(self, tienda):
        mesa = Mesa("M", "Madera", "Roble", 500.0, "rectangular", 4)
        resultado = tienda.agregar_comedor(Comedor("C", mesa))
        assert "exitosamente" in resultado.lower()

    def test_agregar_comedor_invalido(self, tienda):
        resultado = tienda.agregar_comedor("no soy un comedor")
        assert "error" in resultado.lower()


class TestBusquedasYFiltros:

    def test_buscar_por_nombre(self, tienda_con_inventario):
        resultados = tienda_con_inventario.buscar_muebles_por_nombre("silla")
        assert len(resultados) == 2

    def test_buscar_por_nombre_sin_resultados(self, tienda_con_inventario):
        assert tienda_con_inventario.buscar_muebles_por_nombre("inexistente") == []

    def test_buscar_por_nombre_vacio(self, tienda_con_inventario):
        assert tienda_con_inventario.buscar_muebles_por_nombre("  ") == []

    def test_filtrar_por_precio(self, tienda_con_inventario):
        resultados = tienda_con_inventario.filtrar_por_precio(0, 200)
        assert all(m.calcular_precio() <= 200 for m in resultados)
        assert len(resultados) >= 1

    def test_filtrar_por_precio_sin_resultados(self, tienda_con_inventario):
        assert tienda_con_inventario.filtrar_por_precio(100000, 200000) == []

    def test_filtrar_por_material(self, tienda_con_inventario):
        resultados = tienda_con_inventario.filtrar_por_material("madera")
        assert len(resultados) == 2

    def test_filtrar_por_material_vacio(self, tienda_con_inventario):
        assert tienda_con_inventario.filtrar_por_material("") == []

    def test_obtener_muebles_por_tipo(self, tienda_con_inventario):
        assert len(tienda_con_inventario.obtener_muebles_por_tipo(Silla)) == 2
        assert len(tienda_con_inventario.obtener_muebles_por_tipo(Mesa)) == 1


class TestValorYEstadisticas:

    def test_valor_inventario_vacio(self, tienda):
        assert tienda.calcular_valor_inventario() == 0

    def test_valor_inventario(self, tienda_con_inventario):
        esperado = sum(m.calcular_precio() for m in tienda_con_inventario._inventario)
        assert tienda_con_inventario.calcular_valor_inventario() == round(esperado, 2)

    def test_valor_inventario_incluye_comedores(self, tienda):
        mesa = Mesa("M", "Madera", "Roble", 500.0, "rectangular", 4)
        comedor = Comedor("C", mesa)
        tienda.agregar_comedor(comedor)
        assert tienda.calcular_valor_inventario() == comedor.calcular_precio_total()

    def test_estadisticas(self, tienda_con_inventario):
        stats = tienda_con_inventario.obtener_estadisticas()
        assert stats["total_muebles"] == 4
        assert stats["total_comedores"] == 0
        assert stats["ventas_realizadas"] == 0
        assert stats["tipos_muebles"] == {"Silla": 2, "Mesa": 1, "Sofa": 1}

    def test_reporte_inventario(self, tienda_con_inventario):
        reporte = tienda_con_inventario.generar_reporte_inventario()
        assert "Tienda Test" in reporte
        assert "Total de muebles: 4" in reporte
        assert "Silla: 2 unidades" in reporte


class TestDescuentosYVentas:

    def test_aplicar_descuento_valido(self, tienda):
        resultado = tienda.aplicar_descuento("silla", 10)
        assert "10%" in resultado

    def test_aplicar_descuento_invalido(self, tienda):
        assert "error" in tienda.aplicar_descuento("silla", 150).lower()
        assert "error" in tienda.aplicar_descuento("silla", -5).lower()

    def test_venta_sin_descuento(self, tienda_con_inventario):
        mueble = tienda_con_inventario._inventario[0]
        precio = mueble.calcular_precio()
        venta = tienda_con_inventario.realizar_venta(mueble, "Ana")
        assert venta["cliente"] == "Ana"
        assert venta["precio_original"] == precio
        assert venta["precio_final"] == precio
        assert tienda_con_inventario.total_muebles == 3

    def test_venta_con_descuento(self, tienda_con_inventario):
        tienda_con_inventario.aplicar_descuento("silla", 20)
        mueble = tienda_con_inventario._inventario[0]
        precio = mueble.calcular_precio()
        venta = tienda_con_inventario.realizar_venta(mueble, "Luis")
        assert venta["descuento"] == 20
        assert venta["precio_final"] == round(precio * 0.8, 2)

    def test_venta_mueble_no_disponible(self, tienda_con_inventario):
        otro = Silla("Otra", "Madera", "Café", 100.0, True)
        venta = tienda_con_inventario.realizar_venta(otro, "Ana")
        assert "error" in venta

    def test_venta_registrada_en_estadisticas(self, tienda_con_inventario):
        mueble = tienda_con_inventario._inventario[0]
        tienda_con_inventario.realizar_venta(mueble, "Ana")
        assert tienda_con_inventario.obtener_estadisticas()["ventas_realizadas"] == 1
