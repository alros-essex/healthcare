import os
from os.path import exists
import sqlite3

from .doctor import Doctor
from .employee import Employee
from .employee_role import EmployeeRole
from .nurse import Nurse
from .receptionist import Receptionist

from .employee import Employee

class Storage:

    _path_to_database='clinic.db'

    def __init__(self, reset:bool = True):
        if reset:
            os.remove(Storage._path_to_database) 
        path_to_database = Storage._path_to_database
        to_be_initialized = not exists(path_to_database)
        self.con = sqlite3.connect(path_to_database)
        if to_be_initialized:
            self._execute('''CREATE TABLE employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                employee_number TEXT NOT NULL,
                role TEXT NOT NULL)''',
                {})
            # TODO
            if False:
                self._execute('''CREATE TABLE patients(
                    id NUMBER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    address TEXT NOT NULL),
                    phone TEXT NOT NULL''',
                    {})

    def insert_employee(self, employee:Employee):
        self._execute('INSERT INTO employees(name, employee_number, role) VALUES(:name, :employee_number, :role)',
            { 'name': employee.name, 'employee_number': employee.employee_number, 'role': employee.role.value })

    def select_employee(self, role:EmployeeRole = None, employee_number:str = None) -> Employee:
        clause , params = self._select_employee_build_params(role, employee_number)
        cur = self._execute(
            'SELECT name, employee_number, role FROM employees' + (clause if clause is not None else ''), 
            params)
        employees = []
        for row in cur.fetchall():
            employees.append(self._to_employee(row))
        return employees
    
    def _select_employee_build_params(self, role:EmployeeRole = None, employee_number:str = None):
        clause = None
        params = {}
        if role is not None:
            clause = ' where role = :role'
            params['role'] = role.value
        if employee_number is not None:
            clause = (' where ' if clause is None else ' and ') + 'employee_number = :employee_number'
            params['employee_number'] = employee_number
        return clause, params
        
    def _to_employee(self, row):
        role = EmployeeRole[row[2]]
        if role == EmployeeRole.DOCTOR:
            return Doctor(row[0], row[1])
        elif role == EmployeeRole.NURSE:
            return Nurse(row[0], row[1])
        else:
            return Receptionist(row[0], row[1])
            
    def _execute(self, statement, params):
        cur = self.con.cursor()
        cur.execute(statement, params)
        self.con.commit()
        return cur