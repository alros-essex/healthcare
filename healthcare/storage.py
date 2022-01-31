import datetime
import os
from os.path import exists
import sqlite3
from datetime import date, timedelta

from healthcare.prescription import Prescription

from .appointment_type import AppointmentType

from .appointment import Appointment
from .employee import Employee
from .employee_role import EmployeeRole
from .healthcare_professional import HealthcareProfessional
from .patient import Patient
from .employee import Employee

class Storage():
    """persists all the data in a sqlite db"""

    _path_to_database='clinic.db'

    def __init__(self, reset:bool = True):
        """creates the instance
        
        Args:
            reset: if True, the db is re-initialized (if present)
        Returns:
            None"""
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
                name TEXT NOT NULL PRIMARY KEY,
                address TEXT NOT NULL,
                phone TEXT NOT NULL)''',
                {})
            self._execute('''CREATE TABLE appointments(
                type TEXT NOT NULL,
                employee_number INTEGER NOT NULL,
                patient_name TEXT NOT NULL,
                date INTEGER NOT NULL,
                PRIMARY KEY(employee_number, patient_name, date))''',
                {})
            self._execute('''CREATE TABLE prescriptions(
                type TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                dosage INTEGER NOT NULL,
                PRIMARY KEY(type, patient_name, doctor_id))''',
                {})
            self._execute('''CREATE TABLE doctorpatients(
                doctor_id TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                PRIMARY KEY (doctor_id, patient_name))''',
                {})

    def associate_doctor_patient(self, doctor, patient) -> None:
        self._execute('''INSERT INTO doctorpatients(doctor_id, patient_name)
            VALUES(:id, :name)''', {'id': doctor.employee_number, 'name': patient.name})

    def select_employee(self, role:EmployeeRole = None, employee_number:str = None):
        """finds all employees with the given filters
        
        Args:
            role: EmployeeRole (optional)
            employee_number: the employee's number (optional)
        Returns:
            array of Employee"""
        clause , params = self._select_employee_build_params(role, employee_number)
        cur = self._execute(
            'SELECT name, employee_number, role FROM employees' + (clause if clause is not None else ''), 
            params)
        employees = []
        for row in cur.fetchall():
            employees.append(self._to_employee(row))
        return employees

    def insert_employee(self, employee:Employee) -> None:
        """inserts a new record
        
        Args:
            employee: the Employee to store
        Returns:
            None
        """
        self._execute('INSERT INTO employees(name, employee_number, role) VALUES(:name, :employee_number, :role)',
            { 'name': employee.name, 'employee_number': employee.employee_number, 'role': employee.role.name })
    
    def select_doctors(self, employee_number:str = None):
        """shortcut of select_employee(DOCTOR)
        
        Args:
            employee_number: optional employee number
        Returns:
            array of Doctor
        """
        return self.select_employee(role = EmployeeRole.DOCTOR)

    def select_nurses(self, employee_number:str = None):
        """shortcut of select_employee(NURSE)
        
        Args:
            employee_number: optional employee number
        Returns:
            array of Nurse
        """
        return self.select_employee(role = EmployeeRole.NURSE)

    def select_receptionists(self, employee_number:str = None):
        """shortcut of select_employee(RECEPTIONIST)
        
        Args:
            employee_number: optional employee number
        Returns:
            array of Receptionist
        """
        return self.select_employee(role = EmployeeRole.RECEPTIONIST)

    def select_patients(self, doctor = None):
        """finds all the patients
        
        Args:
            doctor: Doctor (optional)
        Returns:
            array of Patient
        """
        if doctor is None:
            cur = self._execute('SELECT name, address, phone from patients', {})
        else:
            cur = self._execute('''SELECT p.name, p.address, p.phone 
                from patients p, doctorpatients dp
                where p.name = dp.patient_name
                and dp.doctor_id = :id''', {'id': doctor.employee_number})
        rows = cur.fetchall()
        patients = []
        for row in rows:
            patient:Patient = self._to_patient(row)
            patients.append(patient)
        return patients

    def select_patient(self, name:str) -> Patient:
        """finds one Patient
        
        Args:
            first_name: first name
            surname: surname
        Returns:
            Patient or None
        """
        params = {}
        params['name'] = name
        cur = self._execute('SELECT address, phone from patients where name = :name', params)
        rows = cur.fetchall()
        return Patient(name, rows[0][0], rows[0][1]) if len(rows) > 0 else None

    def insert_patient(self, patient:Patient) -> None:
        """insert a record
        
        Args:
            patient: a Patient
        Returns:
            None
        """
        self._execute('INSERT INTO patients(name, address, phone) VALUES(:name, :address, :phone)',
            { 'name': patient.name, 'address': patient.address, 'phone': patient.phone })

    def select_appointments(self, filter_employee_numbers=[], filter_date:date=None, filter_patient:Patient=None):
        """finds the matching appointments
        
        Args:
            filter_employee_numbers: select only appointments for these employees (optional)
            filter_date: select only appointments on this day (optional)
            filter_patient: select only appointments for this patient (option)
        Return:
            array of Appointment
        """
        cur = self._execute('''SELECT 
            a.type, a.date,
            e.name, e.employee_number, e.role,
            p.name, p.address, p.phone
            from employees e, patients p, appointments a
            where a.employee_number = e.employee_number
            and a.patient_name = p.name
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
            appointments.append(Appointment(AppointmentType[row[0]], self._to_employee(row[2:5]), self._to_patient(row[5:8]), datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")))
        return appointments

    def select_appointment_dates(self):
        """finds all the date with at least one appointment
        
        Args:
            None
        Returns:
            array of str
        """
        cur = self._execute('select DISTINCT STRFTIME("%d-%m-%Y", date) from appointments',{})
        return [d[0] for d in cur.fetchall()]

    def _build_filter_employee_numbers(self, filter_employee_numbers = []):
        """utility method to build a where clause"""
        return '' if filter_employee_numbers is None else 'and e.employee_number IN ({})'.format(','.join(f'"{f}"' for f in filter_employee_numbers))

    def _build_filter_date(self, filter_date:date = None):
        """utility method to build a where clause"""
        return '' if filter_date is None else 'and a.date >= "{}" and a.date<"{}"'.format(filter_date, filter_date+timedelta(days=1))
    
    def _build_filter_patient(self, filter_patient:Patient = None):
        """utility method to build a where clause"""
        return '' if filter_patient is None else 'and p.name = "{name}"'.format(name = filter_patient.name)

    def insert_appointment(self, appointment:Appointment) -> None:
        """inserts a record
        
        Args:
            appointment: the Appointment
        Returns:
            None
        """
        self._execute('''INSERT INTO appointments(type, employee_number, patient_name, date) VALUES(
            :type, :employee_number, :patient_name, :date)''',
            {'type': appointment.type.value, 'employee_number':appointment.staff.employee_number,
            'patient_name': appointment.patient.name, 'date': appointment.date})

    def delete_appointment(self, appointment:Appointment) -> None:
        """delete one appointment
        
        Args:
            appointment: Appointment
        Returns:
            None
        """
        self._execute('''DELETE FROM appointments 
            where employee_number = :employee_number
            and patient_name = :patient_name
            and date = :date''', 
            {'employee_number': appointment.staff.employee_number, 'patient_name': appointment.patient.name, 'date': appointment.date})

    def select_prescriptions(self, patient:Patient):
        cur = self._execute('''SELECT type, quantity, dosage
            from prescriptions
            where patient_name = :name''',
            {'name': patient.name})
        prescriptions = []
        for row in cur.fetchall():
            prescriptions.append(Prescription(row[0], patient, None, row[1], float(row[2])/100))
        return prescriptions

    def insert_prescription(self, prescription:Prescription):
        self._execute('''INSERT INTO prescriptions(type, patient_name, doctor_id, quantity, dosage)
            VALUES(:type, :name, :id, :quantity, :dosage)''',
            {'type': prescription.type, 'name':prescription.patient.name, 'id': prescription.doctor.employee_number,
            'quantity': prescription.quantity, 'dosage':prescription.dosage*100})

    def _select_employee_build_params(self, role:EmployeeRole = None, employee_number:str = None):
        """helper to build a where clause"""
        clause = None
        params = {}
        if role is not None:
            clause = ' where role = :role'
            params['role'] = role.name
        if employee_number is not None:
            clause = (' where ' if clause is None else ' and ') + 'employee_number = :employee_number'
            params['employee_number'] = employee_number
        return clause, params
        
    def _to_employee(self, row):
        """helper to convert a row"""
        from .nurse import Nurse
        from .receptionist import Receptionist
        from .doctor import Doctor
        role = EmployeeRole[row[2]]
        if role == EmployeeRole.DOCTOR:
            return Doctor(row[0], row[1], storage=self)
        elif role == EmployeeRole.NURSE:
            return Nurse(row[0], row[1])
        else:
            return Receptionist(row[0], row[1], storage=self)

    def _to_patient(self, row) -> Patient:
        """helper to convert a row"""
        return Patient(name = row[0], address = row[1], phone = row[2])
            
    def _execute(self, statement, params):
        """calls the database
        
        Args:
            statement: command to execute
            params: parameters for the command as a dict
        Returns:
            None
        """
        cur = self.con.cursor()
        cur.execute(statement, params)
        self.con.commit()
        return cur
