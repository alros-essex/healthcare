import datetime
import os
from os.path import exists
import sqlite3
from datetime import date, timedelta

from .appointment_type import AppointmentType

from .appointment import Appointment
from .employee import Employee
from .employee_role import EmployeeRole
from .healthcare_professional import HealthcareProfessional
from .patient import Patient
from .employee import Employee

class Storage():

    _path_to_database='clinic.db'

    def __init__(self, reset:bool = True):
        if reset:
            os.remove(Storage._path_to_database) 
        path_to_database = Storage._path_to_database
        to_be_initialized = not exists(path_to_database)
        self.con = sqlite3.connect(path_to_database)
        if to_be_initialized:
            self._execute('''CREATE TABLE employees(
                employee_number TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL)''',
                {})
            self._execute('''CREATE TABLE patients(
                first_name TEXT NOT NULL,
                surname TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                PRIMARY KEY(first_name, surname))''',
                {})
            self._execute('''CREATE TABLE appointments(
                type TEXT NOT NULL,
                employee_number INTEGER NOT NULL,
                patient_id INTEGER NOT NULL,
                date INTEGER NOT NULL,
                PRIMARY KEY(employee_number, patient_id, date))''',
                {})

    def select_employee(self, role:EmployeeRole = None, employee_number:str = None):
        clause , params = self._select_employee_build_params(role, employee_number)
        cur = self._execute(
            'SELECT name, employee_number, role FROM employees' + (clause if clause is not None else ''), 
            params)
        employees = []
        for row in cur.fetchall():
            employees.append(self._to_employee(row))
        return employees

    def insert_employee(self, employee:Employee):
        self._execute('INSERT INTO employees(name, employee_number, role) VALUES(:name, :employee_number, :role)',
            { 'name': employee.name, 'employee_number': employee.employee_number, 'role': employee.role.value })
    
    def select_doctors(self, employee_number:str = None):
        return self.select_employee(role = EmployeeRole.DOCTOR)

    def select_nurses(self, employee_number:str = None):
        return self.select_employee(role = EmployeeRole.NURSE)

    def select_receptionists(self, employee_number:str = None):
        return self.select_employee(role = EmployeeRole.RECEPTIONIST)

    def select_patients(self):
        cur = self._execute('SELECT first_name, surname, address, phone from patients', {})
        rows = cur.fetchall()
        patients = []
        for row in rows:
            patients.append(self._to_patient(row))
        return patients

    def select_patient(self, first_name:str, surname:str) -> Patient:
        params = {}
        params['first_name'] = first_name
        params['surname'] = surname
        cur = self._execute('SELECT address, phone from patients where first_name = :first_name and surname = :surname', params)
        rows = cur.fetchall()
        return Patient(first_name, surname, rows[0][0], rows[0][1]) if len(rows) > 0 else None

    def insert_patient(self, patient:Patient) -> None:
        self._execute('INSERT INTO patients(first_name, surname, address, phone) VALUES(:first_name, :surname, :address, :phone)',
            { 'first_name': patient.firstname, 'surname': patient.surname, 'address': patient.address, 'phone': patient.phone })

    def select_appointments(self, filter_employee_numbers=[], filter_date:date=None, filter_patient:Patient=None):
        cur = self._execute('''SELECT 
            a.type, a.date,
            e.name, e.employee_number, e.role,
            p.first_name, p.surname, p.address, p.phone
            from employees e, patients p, appointments a
            where a.employee_number = e.employee_number
            and patient_id = p.rowid
            {filter_employee_numbers}
            {filter_date}
            {filter_patient}
            ORDER BY a.date, e.name
        '''.format(
            filter_employee_numbers=self._build_filter_employee_numbers(filter_employee_numbers),
            filter_date=self._build_filter_date(filter_date), 
            filter_patient=self._build_filter_patient(filter_patient)), {})
        rows = cur.fetchall()
        appointments = []
        for row in rows:
            appointments.append(Appointment(AppointmentType[row[0]], self._to_employee(row[2:5]), self._to_patient(row[5:9]), datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")))
        return appointments

    def _build_filter_employee_numbers(self, filter_employee_numbers = []):
        return '' if filter_employee_numbers is None else 'and e.employee_number IN ({})'.format(','.join(f'"{f}"' for f in filter_employee_numbers))

    def _build_filter_date(self, filter_date:date = None):
        return '' if filter_date is None else 'and a.date >= "{}" and a.date<"{}"'.format(filter_date, filter_date+timedelta(days=1))
    
    def _build_filter_patient(self, filter_patient:Patient = None):
        return '' if filter_patient is None else 'and p.first_name = "{first_name}" and p.surname = "{surname}"'.format(
            first_name = filter_patient.firstname, surname = filter_patient.surname)

    def insert_appointment(self, appointment:Appointment) -> None:
        self._execute('''INSERT INTO appointments(type, employee_number, patient_id, date) VALUES(
            :type, :employee_number, 
            (SELECT rowid from patients p where p.first_name = :patient_first_name and p.surname = :patient_surname), 
            :date)''',
            {'type': appointment.type.value, 'employee_number':appointment.staff.employee_number,
            'patient_first_name': appointment.patient.firstname, 'patient_surname': appointment.patient.surname,
            'date': appointment.date})

    def delete_appointment(self, appointment:Appointment) -> None:
        self._execute('''DELETE FROM appointments 
            where employee_number = :employee_number
            and patient_id = (SELECT rowid from patients p where p.first_name = :first_name and p.surname = :surname)
            and date = :date''', 
            {'employee_number': appointment.staff.employee_number, 'first_name': appointment.patient.firstname,
            'surname': appointment.patient.surname, 'date': appointment.date})

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
        from .nurse import Nurse
        from .receptionist import Receptionist
        from .doctor import Doctor
        role = EmployeeRole[row[2]]
        if role == EmployeeRole.DOCTOR:
            return Doctor(row[0], row[1])
        elif role == EmployeeRole.NURSE:
            return Nurse(row[0], row[1])
        else:
            return Receptionist(row[0], row[1], None)

    def _to_patient(self, row) -> Patient:
        return Patient(firstname = row[0], surname = row[1], address = row[2], phone = row[3])
            
    def _execute(self, statement, params):
        cur = self.con.cursor()
        cur.execute(statement, params)
        self.con.commit()
        return cur
