"""
    This class is serving as a base class for out entites,
    such as Patient, Doctor in our 
    Hospital Appointment system.
"""
import json
import uuid # For generating unique IDs

"""
    Import type hints for better code readability 
    List: For specifying lists of a certain type 
    Optional: For indicating that a value can either be a specific type or none
    Dict: For specifying dictionaries with key and value types
"""
from typing import List, Optional, Dict

class Person:
    # Constructor method initaializing  the new person instance 
    def __init__(self, name: str, contact_info: str, age :int, gender: str):
        self.name = name
        self.contact_info = contact_info
        self.age = age
        self.gender = gender

        # This generates a unique identifier for each person
        self.person_id = str(uuid.uuid4())[:11]

    def get_name(self) -> str:
        return self.name # Returns the name of the person
        
    def get_contact_info(self) -> str:
        return self.contact_info # Returns the contact information of the person
    
    def get_age(self) -> int:
        return self.age # Returns the age of the person

    def get_gender(self) -> str:
        return self.gender # Returns the gender of the person

    # Defining the Mutators method to update the value of the Person
    def set_name(self, name: str):
        self.name = name # Updates the name of the person

    def set_contact_info(self, contact_info: str):
        self.contact_info = contact_info

    def set_age(self, age: int):
        if age < 0:
            raise ValueError("Age cannot be negative. ")
        self.age = age
    
    def set_gender(self, gender: str):
        self.gender = gender
    
        # updating a person's information. If a parameter is provided 

    def update_info(self, name =None, contact_info = None, age = None, gender =None):
        if name:
            self.name = name
        if contact_info:
            self.contact_info = contact_info
        if age:
            self.age = age
        if gender:
            self.gender = gender

    def __str__(self) -> str:
        # Returning a humnan-readable string representation of the person instance
        return f"Name: {self.name},\n Contact Info: {self.contact_info},\n Age: {self.age},\n Gender: {self.gender}"
    """
        This _str_ method is used to return a human-readable string representation of the person instance.
    """



class Doctor(Person):
    def __init__(self, name: str, contact_info: str, age: int, gender: str, specialization: str):
        super().__init__(name, contact_info, age, gender)
        self.specialization = specialization
        self.schedule: List[Dict[str, str]]= []  # List that stores the available time slots

    def add_available_slot(self, date: str, time: str):
        slot = {"date" : date, "time": time}
        if slot not in self.schedule:  # Check if slot already exists
                self.schedule.append(slot)
        
    def remove_slot(self, date: str, time: str):
        slot = {"date": date, "time": time}
        if slot in self.schedule:
            self.schedule.remove(slot)
        
    def get_schedule(self) -> List[Dict[str, str]]:
        return self.schedule # Returns the doctor's schedule.

    def __str__(self):
        return f"Doctor {self.name} ({self.specialization})\nContact: {self.contact_info}\nAvailable Slots: {', '.join(self.schedule)}"


class Patient(Person):
    #passing the person class as a parent class to the patient class.
    def __init__(self, name: str, contact_info: str, age: int, gender: str, card_no: int, date_of_birth: str,  required_specialization: str):
        super().__init__(name, contact_info, age, gender)
        # Re-using the initialization of the parent class 
        self.card_no = card_no
        self.date_of_birth = date_of_birth
        self.required_specialization = required_specialization # specialization required by the patient
        self.appointments: List[Dict[str, str]] = []  # list that stores appointments

    def add_appointment(self, appointment_date: str, appointment_time: str):
        appointment = {
            'date': appointment_date,
            'time': appointment_time,
        }
        self.appointments.append(appointment)  # Add appointment to patient

    def cancel_appointment(self, appointment_date: str, appointment_time: str):
        appointment_to_remove = next((appt for appt in self.appointments if appt['date'] == appointment_date and appt['time'] == appointment_time), None)
        if appointment_to_remove:
            self.appointments.remove(appointment_to_remove)  # Removes appointment from patient

    # def view_appointments(self) -> List[Dict[str, str]]:
    #     return self.appointments  # views all scheduled appointments

class Appointment:
    def __init__(self, patient: Patient, doctor: Doctor, date: str, time: str, status: str = "Scheduled"):
        self.appointment_id = str(uuid.uuid4()) # Unique ID for each appointment
        self.patient = patient  # Composition: using Patient object
        self.doctor = doctor  # Composition: using Doctor object
        self.time = time
        self.status = status
        self.date = date

    def cancel_appointment(self):
        if self.status == "Scheduled":
            self.status = "Cancelled"
            print(f"Appointment {self.appointment_id} has been cancelled.")
        else:
            print(f"Appointment {self.appointment_id} is already {self.status}.")

    def reschedule_appointment(self, new_date : str, new_time: str):
        """Reschedule the appointment to new date/time."""
        if self.status == "Scheduled":
            # Free up original slot
            self.doctor.add_available_slot(self.date, self.time)
            
            # Check new slot availability
            if {"date": new_date, "time": new_time} in self.doctor.get_schedule():
                self.date = new_date
                self.time = new_time
                self.doctor.remove_slot(new_date, new_time)
                return True
        return False
    def __str__(self):
        return f"""
                Appointment ID: {self.appointment_id}
                Patient Name: {self.patient.name}
                Doctor Name: {self.doctor.name}
                Date: {self.date}
                Time: {self.time}
                Status: {self.status}
               """
class AppointmentScheduler:
    def __init__(self):
        self.appointments: List[Appointment] = []  # List to store all scheduled appointments
        self.doctors: List[Doctor] = []       # List to store available doctors
        self.patients: List[Patient]= []      # List to store registered patients

    def add_doctor(self, doctor : Doctor):
        self.doctors.append(doctor)  # Add a doctor to the scheduler

    def add_patient(self, patient: Patient):
        self.patients.append(patient)  # Add a patient to the scheduler
    
    def find_doctors_by_specialization(self, specialization: str) -> List[Doctor]:
        """Return doctors with the given specialization."""
        return [doctor for doctor in self.doctors if doctor.specialization == specialization]

    def schedule_appointment(self, patient, date: str, time: str):
        """
    Schedule an appointment for a patient with a doctor matching their required specialization.
    """
        
        # Find doctors matching the patient's required specialization
        matching_doctors = self.find_doctors_by_specialization(patient.required_specialization)

        if not matching_doctors:
            print(f"No {patient.required_specialization} available at this time.")
            return None
        
        # Find the first available doctor
        for doctor in matching_doctors:
            if {"date" : date, "time": time} in doctor.get_schedule():
                new_appointment = Appointment(patient, doctor, date, time)
                self.appointments.append(new_appointment)  # Add appointment to the list
                patient.add_appointment( date, time)  # Add to patient's appointments
                doctor.remove_slot(date, time) #Mark slot as booked 
                print(f"Assigned Dr. {doctor.name} ({doctor.specialization}) to patient {patient.name}.")
                return new_appointment
            else:
                print(f"No doctors available for {patient.required_specialization} at {date} {time}.")
                return None
            
    def reschedule_appointment(self, appointment_id, new_date, new_time):
        # Find the appointment
        appointment = next((a for a in self.appointments 
                        if a.appointment_id == appointment_id), None)
        if appointment:
            # Call the Appointment class method
            return appointment.reschedule_appointment(new_date, new_time)
        return False, "Appointment not found."
    
    def cancel_appointment(self, appointment_id):
        appointment_to_cancel = next((appt for appt in self.appointments if appt.appointment_id == appointment_id), None)
        if appointment_to_cancel:
            appointment_to_cancel.cancel_appointment()
            self.appointments.remove(appointment_to_cancel)
            print(f"Appointment {appointment_id} has been cancelled.")  # Remove from the list
        else:
            print(f"No appointment found with ID {appointment_id}.")

    def view_appointments(self):
        for appointment in self.appointments:
            print(appointment)

class DataManager:
    def load_patients_from_json():
        try:
             with open('patients.json', 'r') as f:
                patients_data = json.load(f)
                patients = []
                for patient_data in patients_data:
                    patient = Patient(
                        name=patient_data['name'],
                        contact_info=patient_data['contact_info'],
                        age=patient_data['age'],
                        gender=patient_data['gender'],
                        card_no=patient_data['card_no'],
                        date_of_birth=patient_data['date_of_birth'],
                        required_specialization=patient_data['Specialization of Doctor Needed']
                    )
                    patient.person_id = patient_data['patient_id']
                    patients.append(patient)
                return patients
        except FileNotFoundError:
            print("Patient database not found. Starting with an empty list.")
            return []
        except json.JSONDecodeError:
            print("Patient database is corrupted. Starting with an empty list.")
            return []
    def save_patients_to_json(patients):
        patients_data = []
        for patient in patients:
            patient_data = {
                "name": patient.name,
                "contact_info": patient.contact_info,
                "age": patient.age,
                "gender": patient.gender,
                "card_no": patient.card_no,
                "date_of_birth": patient.date_of_birth,
                "Specialization of Doctor Needed": patient.required_specialization,
                "patient_id": patient.person_id
            }
            patients_data.append(patient_data)
        
        with open('patients.json', 'w') as f:
            json.dump(patients_data, f, indent=4)

    def load_doctors_from_json():
        """
        Load doctor data from doctors.json and return a list of Doctor objects.
        """
        try:
            with open('doctors.json', 'r') as f:
                doctors_data = json.load(f)
                doctors = []
                for doctor_data in doctors_data:
                    doctor = Doctor(
                        name=doctor_data['name'],
                        contact_info=doctor_data['contact_info'],
                        age=doctor_data['age'],
                        gender=doctor_data['gender'],
                        specialization=doctor_data['specialization']
                    )
                    doctor.person_id = doctor_data['doctor_id']
                    doctor.schedule = doctor_data['schedule']
                    doctors.append(doctor)
                return doctors
        except FileNotFoundError:
            print("Doctor database not found. Starting with an empty list.")
            return []
        except json.JSONDecodeError:
            print("Doctor database is corrupted. Starting with an empty list.")
            return []

    def save_doctors_to_json(doctors):
        """
        Save a list of Doctor objects to doctors.json.
        """
        doctors_data = []
        for doctor in doctors:
            doctor_data = {
                "name": doctor.name,
                "contact_info": doctor.contact_info,
                "age": doctor.age,
                "gender": doctor.gender,
                "specialization": doctor.specialization,
                "schedule": doctor.schedule,
                "doctor_id": doctor.person_id
            }
            doctors_data.append(doctor_data)
        
        with open('doctors.json', 'w') as f:
            json.dump(doctors_data, f, indent=4)
        
    def load_appointments_from_json(patients, doctors):
        """
        Load appointment data from appointments.json and return a list of Appointment objects.
        """
        try:
            with open('appointments.json', 'r') as f:
                appointments_data = json.load(f)
                appointments = []
                for appointment_data in appointments_data:
                    patient = next((p for p in patients 
                                   if p.person_id == appointment_data['patient_id']), None)
                    doctor = next((d for d in doctors 
                                  if d.person_id == appointment_data['doctor_id']), None)
                    
                    if patient and doctor:
                        appointment = Appointment(
                            patient=patient,
                            doctor=doctor,
                            date=appointment_data['date'],
                            time=appointment_data['time'],
                            status=appointment_data['status']
                        )
                        appointment.appointment_id = appointment_data['appointment_id']
                        appointments.append(appointment)
                return appointments
        except FileNotFoundError:
            print("Appointment database not found. Starting with an empty list.")
            return []
        except json.JSONDecodeError:
            print("Appointment database is corrupted. Starting with an empty list.")
            return []
    
    def save_appointments_to_json(appointments):
        """
        Save a list of Appointment objects to appointments.json.
        """
        appointments_data = []
        for appointment in appointments:
            appointment_data = {
                "appointment_id": appointment.appointment_id,
                "patient_id": appointment.patient.person_id,
                "doctor_id": appointment.doctor.person_id,
                "date": appointment.date,
                "time": appointment.time,
                "status": appointment.status
            }
            appointments_data.append(appointment_data)
        
        with open('appointments.json', 'w') as f:
            json.dump(appointments_data, f, indent=4)
# # Testing the whole class
# # ----------------------------
# # Step 1: Create Doctors
# # ----------------------------
# # Create a Cardiologist with availability
# cardio_doctor = Doctor(
#     name="Dr. Heart", 
#     contact_info="heart@hospital.com",
#     age=45,
#     gender="Male",
#     specialization="Cardiology"
# )
# cardio_doctor.add_available_slot("2023-12-25", "10:00 AM")
# cardio_doctor.add_available_slot("2023-12-25", "2:00 PM")

# # Create a Neurologist with availability
# neuro_doctor = Doctor(
#     name="Dr. Brain", 
#     contact_info="brain@hospital.com",
#     age=38,
#     gender="Female",
#     specialization="Neurology"
# )
# neuro_doctor.add_available_slot("2023-12-25", "11:00 AM")

# # ----------------------------
# # Step 2: Create Patients with Required Specializations
# # ----------------------------
# # Patient needing cardiology
# patient1 = Patient(
#     name="John Smith",
#     contact_info="john@email.com",
#     age=55,
#     gender="Male",
#     card_no=1001,
#     date_of_birth="1968-03-12",
#     required_specialization="Cardiology"  # Key feature for auto-assignment
# )

# # Patient needing neurology
# patient2 = Patient(
#     name="Emma Brown",
#     contact_info="emma@email.com",
#     age=42,
#     gender="Female",
#     card_no=1002,
#     date_of_birth="1981-07-24",
#     required_specialization="Neurology"
# )

# # ----------------------------
# # Step 3: Initialize Scheduler
# # ----------------------------
# scheduler = AppointmentScheduler()
# scheduler.add_doctor(cardio_doctor)
# scheduler.add_doctor(neuro_doctor)
# scheduler.add_patient(patient1)
# scheduler.add_patient(patient2)

# # ----------------------------
# # Step 4: Auto-Assign Appointments
# # ----------------------------
# print("\n--- Booking Cardiology Appointment ---")
# # System automatically assigns cardiology doctor
# scheduler.schedule_appointment(patient1, "2023-12-25", "10:00 AM")

# print("\n--- Booking Neurology Appointment ---")
# scheduler.schedule_appointment(patient2, "2023-12-25", "10:00 AM")
