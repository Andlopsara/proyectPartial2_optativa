# dao/employee_dao.py

import mysql.connector
from db_connection import get_conn, close_conn # Para usar el Pool de Conexiones
# Importa TODAS las clases de empleados
from employee import Employee 
from receptionist import Receptionist
from bellboy import Bellboy
from typing import Optional, List

class EmployeeDAO:
    """DAO para la entidad EMPLOYEES, incluyendo sus subclases."""

    # Mapeo de roles de la BD a Clases de Python
    ROLE_MAPPING = {
        "Receptionist": Receptionist,
        "Bellboy": Bellboy,
        "Employee": Employee,
        "Manager": Employee  # Si no tienes clase Manager, usa Employee
    }

    # C - CREATE: Inserta un nuevo Empleado (o subclase)
    def create(self, emp: Employee) -> Optional[int]:
        conn = get_conn()
        cursor = conn.cursor()
        
        # El rol se determina por el tipo de instancia (Receptionist, Bellboy, Employee)
        role = type(emp).__name__
        if role not in self.ROLE_MAPPING:
            role = "Employee"

        query = """
            INSERT INTO EMPLOYEES 
            (first_name, second_name, last_name, second_last_name, phone, email, curp, password_hash, status, role) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            emp.getFirstName(), emp.getSecondName(), emp.getLastName(), 
            emp.getSecondLastName(), emp.getPhone(), emp.getEmail(), 
            emp.getCurp(), emp.getPassword(), emp.getStatus(), role
        )
        
        try:
            cursor.execute(query, values)
            conn.commit()
            emp_id = cursor.lastrowid
            emp.setId(emp_id)
            return emp_id
        except mysql.connector.Error as err:
            print(f"Error CREATE Employee: {err}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            close_conn(conn)

    # R - READ: Obtiene un Empleado (o subclase) por ID
    def get_by_id(self, emp_id: int) -> Optional[Employee]:
        conn = get_conn()
        cursor = conn.cursor()
        
        query = """
            SELECT employee_id, first_name, second_name, last_name, second_last_name, 
                   phone, email, status, curp, password_hash, role 
            FROM EMPLOYEES 
            WHERE employee_id = %s
        """
        
        try:
            cursor.execute(query, (emp_id,))
            record = cursor.fetchone()
            
            if record:
                (id, fName, sName, lName, sLName, phone, email, status, curp, password, role) = record
                
                # 1. Determina la clase a instanciar (Employee, Receptionist, o Bellboy)
                EmployeeClass = self.ROLE_MAPPING.get(role, Employee)
                
                # 2. Instancia el objeto usando el constructor de la clase base Employee
                return EmployeeClass(id, fName, sName, lName, sLName, phone, email, status, curp, password)
            return None
        except mysql.connector.Error as err:
            print(f"Error READ Employee: {err}")
            return None
        finally:
            cursor.close()
            close_conn(conn)
            
    # U - UPDATE: Actualiza el estado de un Empleado
    def update_status(self, emp_id: int, new_status: str) -> bool:
        conn = get_conn()
        cursor = conn.cursor()
        query = "UPDATE EMPLOYEES SET status=%s WHERE employee_id=%s"
        values = (new_status, emp_id)
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error UPDATE Employee Status: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            close_conn(conn)
            
    # D - DELETE: Elimina un Empleado (Opcional: puedes preferir solo cambiar el status)
    def delete(self, emp_id: int) -> bool:
        conn = get_conn()
        cursor = conn.cursor()
        query = "DELETE FROM EMPLOYEES WHERE employee_id = %s"
        try:
            cursor.execute(query, (emp_id,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error DELETE Employee: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            close_conn(conn)