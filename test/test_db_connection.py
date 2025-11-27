import pytest
from unittest.mock import MagicMock
from db_connection import get_conn, close_conn, DBConnection
from mysql.connector.errors import InterfaceError 


@pytest.fixture(autouse=True)
def mock_db_pool(mocker):
    """
    Fixture que simula (mokea) la clase MySQLConnectionPool de la libreria externa.

    Se parchea el objeto real para aislar la prueba, retornando un objeto Mock 
    que simula el comportamiento de un Pool y la Conexion.
    """
    MockPool = mocker.MagicMock() 
    MockConnection = mocker.MagicMock()
    MockPool.return_value.get_connection.return_value = MockConnection
    
    # Este es el mock que representa la CLASE MySQLConnectionPool
    mock_class = mocker.patch(
        'db_connection.MySQLConnectionPool', 
        return_value=MockPool.return_value
    )

    # Asegura que cada prueba comience con un estado limpio, reseteando el Singleton.
    DBConnection._instance = None

    return mock_class

def test_singleton_pattern_pool_initialization(mock_db_pool):
    """
    Verifica el patron Singleton: el pool de conexiones solo debe ser inicializado una vez.
    
    La aserción clave es que la clase MySQLConnectionPool simulada (mock_db_pool) 
    haya sido llamada para su construccion una sola vez, incluso tras multiples 
    llamadas a la funcion publica get_conn().
    """
    conn1 = get_conn()
    
    conn2 = get_conn()

    mock_db_pool.assert_called_once() # Verifica que el constructor fue llamado una vez
    assert mock_db_pool.return_value.get_connection.call_count == 2
    

def test_connection_is_returned_to_pool(mock_db_pool):
    """
    Verifica el contrato de close_conn(): Al cerrar la conexion, se debe llamar 
    al metodo .close() de la conexion prestada, devolviendola al pool.
    """
    mock_conn = get_conn()
    close_conn(mock_conn)
    mock_conn.close.assert_called_once()


def test_initialization_failure_raises_exception(mocker):
    """
    Prueba que si la inicialización del Pool falla (ej. DB caida o credenciales invalidas), 
    la excepcion sea propagada o manejada correctamente.
    
    Se simula que el constructor de MySQLConnectionPool lanza un InterfaceError.
    """
    # Asegura un estado limpio para esta prueba también.
    DBConnection._instance = None

    mocker.patch(
        'db_connection.MySQLConnectionPool', 
        side_effect=InterfaceError("Host caido o credenciales invalidas")
    )

    with pytest.raises(InterfaceError):
        get_conn()