import unittest
from unittest.mock import MagicMock, patch
import mysql.connector

# Importar las clases de los componentes a probar
from customer import Customer
from payment import Payment
from reservationService import ServiceReservation
from reservation import Reservation
from dao.customer_dao import CustomerDAO # Asegúrate que la ruta al DAO es correcta
from dao.reservation_dao import ReservationDAO

# --------------------------------------------------------------------------
# I. Pruebas de la Capa DAO (Persistencia y Transacciones)
# --------------------------------------------------------------------------

# Usamos @patch para simular las funciones de conexión del módulo db_connection
@patch('dao.customer_dao.get_conn')
@patch('dao.customer_dao.close_conn')
class TestCustomerDAOLogic(unittest.TestCase):
    
    # SETUP de MOCK para la conexión y el cursor
    def setUp(self):
        self.dao = CustomerDAO()
        self.mock_customer = Customer(0, "Test", "S", "User", "A", "123", "test@mail.com", "State", "CURP123", "hash")

    # TEST 1: Validación de creación exitosa y Mapeo Objeto-Relacional (ORM)
    def test_01_create_customer_success(self, mock_close_conn, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 42
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        new_id = self.dao.create(self.mock_customer)
        self.assertEqual(new_id, 42)
        self.assertEqual(self.mock_customer.getId(), 42)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        
    # TEST 2: Manejo de Excepciones de la BD (Transaccionalidad)
    def test_02_create_customer_db_error_handles_rollback(self, mock_close_conn, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mysql.connector.Error("Simulated DB Error")
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        new_id = self.dao.create(self.mock_customer)
        self.assertIsNone(new_id)
        mock_conn.rollback.assert_called_once()
        self.assertEqual(self.mock_customer.getId(), 0)

# Pruebas de Entidades de Dominio (Lógica de Negocio y Colaboración)

class TestReservationLogic(unittest.TestCase):
    def setUp(self):
        self.mock_room = MagicMock()
        self.mock_customer = MagicMock()
        self.reservation = Reservation(1, "2025-01-01", "2025-01-05", self.mock_customer, self.mock_room)

    #3  Validación de Transición de Estado y Colaboración
    def test_03_create_reservation_success_collaboration(self):
        self.mock_room.getStatus.return_value = "Available"
        success = self.reservation.createReservation()
        self.assertTrue(success)
        self.mock_room.assignCustomer.assert_called_once_with(self.mock_customer)
        self.mock_customer.makeReservation.assert_called_once_with(self.reservation)
    def test_04_payment_encapsulation_and_date_assignment(self):
        with patch('payment.date') as mock_date:
            mock_date.today.return_value = '2025-11-26'
            pay = Payment(100, 500.50, "Credit Card")
            pay.setAmount(600.75)
            self.assertEqual(pay.getAmount(), 600.75)
            self.assertEqual(pay.getDate(), '2025-11-26')
            
    # 4 Validación de Lógica de Colecciones 
    def test_05_customer_reservation_list_management(self):
        cust = Customer(1, "Test", "", "User", "", "123", "e@mail.com", "State", "CURP123")
        mock_res_1 = MagicMock()
        mock_res_1.getId.return_value = 101
        cust.makeReservation(mock_res_1)
        self.assertEqual(len(cust._Customer__reservations), 1)
        success = cust.cancelReservation(101)
        self.assertTrue(success)
        self.assertEqual(len(cust._Customer__reservations), 0)
        fail = cust.cancelReservation(999)
        self.assertFalse(fail)

if __name__ == '__main__':
    unittest.main()