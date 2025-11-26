import mysql.connector
from db_connection import get_conn, close_conn
from employee import Employee 
from receptionist import Receptionist
from bellboy import Bellboy
from typing import Optional, List

class EmployeeDAO:
    ROLE_MAPPING = {
        "Receptionist": Receptionist,
        "Bellboy": Bellboy,
        "Employee": Employee,
        "Manager": Employee
    }

    def create(self, emp: Employee) -> Optional[int]:
        conn = None
        cursor = None
        role = type(emp).__name__
        if role not in self.ROLE_MAPPING: # type: ignore
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
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            emp_id = cursor.lastrowid
            emp.setId(emp_id)
            return emp_id
        except mysql.connector.Error as err:
            print(f"Error CREATE Employee: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)

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
                EmployeeClass = self.ROLE_MAPPING.get(role, Employee)
                return EmployeeClass(id, fName, sName, lName, sLName, phone, email, status, curp, password)
            return None
        except mysql.connector.Error as err:
            print(f"Error READ Employee: {err}")
            return None
        finally:
            cursor.close()
            close_conn(conn)
            
    def get_all(self) -> List[Employee]:
        conn = None
        cursor = None
        employees = []
        query = """
            SELECT employee_id, first_name, second_name, last_name, second_last_name, 
                   phone, email, status, curp, password_hash, role 
            FROM EMPLOYEES
        """
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                (id, fName, sName, lName, sLName, phone, email, status, curp, password, role) = record
                EmployeeClass = self.ROLE_MAPPING.get(role, Employee)
                employees.append(
                    EmployeeClass(id, fName, sName, lName, sLName, phone, email, status, curp, password)
                )
            print(f"INFO: Se cargaron {len(employees)} empleados desde la BD.")
        except mysql.connector.Error as err:
            print(f"Error READ ALL Employees: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)
        return employees

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