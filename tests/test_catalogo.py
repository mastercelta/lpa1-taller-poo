import pytest
from services.catalogo import Catalogo
from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.sofa import Sofa


@pytest.fixture
def muebles():
    return [
        Silla("Silla Clásica", "Madera", "Café", 100.0, True),
        Silla("Silla Metal", "Metal", "Negro", 200.0, True),
        Mesa("Mesa Roble", "Madera", "Roble", 500.0, "rectangular", 4),
        Sofa("Sofá Gris", "Tela", "Gris", 800.0),
    ]


@pytest.fixture
def catalogo(muebles):
    return Catalogo(muebles)


class TestCreacion:

    def test_catalogo_vacio(self):
        catalogo = Catalogo()
        assert len(catalogo) == 0
        assert catalogo.muebles == []

    def test_catalogo_con_muebles(self, catalogo):
        assert len(catalogo) == 4

    def test_muebles_retorna_copia(self, catalogo):
        catalogo.muebles.clear()
        assert len(catalogo) == 4

    def test_refleja_cambios_en_la_lista_original(self):
        tienda = TiendaMuebles("Tienda")
        catalogo = Catalogo(tienda._inventario)
        tienda.agregar_mueble(Silla("S", "Madera", "Café", 100.0, True))
        assert len(catalogo) == 1


class TestBusqueda:

    def test_buscar_por_nombre(self, catalogo):
        assert len(catalogo.buscar_por_nombre("silla")) == 2

    def test_buscar_sin_resultados(self, catalogo):
        assert catalogo.buscar_por_nombre("inexistente") == []

    def test_buscar_vacio(self, catalogo):
        assert catalogo.buscar_por_nombre("  ") == []


class TestFiltros:

    def test_filtrar_por_precio(self, catalogo):
        resultados = catalogo.filtrar_por_precio(0, 200)
        assert len(resultados) >= 1
        assert all(m.calcular_precio() <= 200 for m in resultados)

    def test_filtrar_por_precio_sin_resultados(self, catalogo):
        assert catalogo.filtrar_por_precio(100000, 200000) == []

    def test_filtrar_por_material(self, catalogo):
        assert len(catalogo.filtrar_por_material("madera")) == 2

    def test_filtrar_por_material_vacio(self, catalogo):
        assert catalogo.filtrar_por_material("") == []

    def test_filtrar_por_tipo(self, catalogo):
        assert len(catalogo.filtrar_por_tipo(Silla)) == 2
        assert len(catalogo.filtrar_por_tipo(Mesa)) == 1


class TestOrden:

    def test_ordenar_ascendente(self, catalogo):
        precios = [m.calcular_precio() for m in catalogo.ordenar_por_precio()]
        assert precios == sorted(precios)

    def test_ordenar_descendente(self, catalogo):
        precios = [m.calcular_precio() for m in catalogo.ordenar_por_precio(descendente=True)]
        assert precios == sorted(precios, reverse=True)

    def test_ordenar_no_modifica_el_original(self, catalogo, muebles):
        catalogo.ordenar_por_precio(descendente=True)
        assert catalogo.muebles == muebles
