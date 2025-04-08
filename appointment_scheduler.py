from patient import Patient
from Doctor_class import Doctor
from Appointment import Appointment
class AppointmentScheduler(Patient, Doctor):
    def __init__(self):
        self.appointments = []  # List to store all scheduled appointments
        self.doctors = []       # List to store available doctors
        self.patients = []      # List to store registered patients

    def add_doctor(self, doctor):
        self.doctors.append(doctor)  # Add a doctor to the scheduler

    def add_patient(self, patient):
        self.patients.append(patient)  # Add a patient to the scheduler

    def schedule_appointment(self, patient, doctor, time):
        if time in doctor.get_schedule():
            appointment_id = len(self.appointments) + 1  # Simple ID generation
            new_appointment = Appointment(appointment_id, patient, doctor, time)
            self.appointments.append(new_appointment)  # Add appointment to the list
            patient.add_appointment("Date Placeholder", time)  # Add to patient's appointments
            print(f"Appointment scheduled: {new_appointment}")
        else:
            print(f"Doctor {doctor} is not available at {time}.")

    def cancel_appointment(self, appointment_id):
        appointment_to_cancel = next((appt for appt in self.appointments if appt.appointment_id == appointment_id), None)
        if appointment_to_cancel:
            appointment_to_cancel.cancel_appointment()
            self.appointments.remove(appointment_to_cancel)  # Remove from the list
        else:
            print(f"No appointment found with ID {appointment_id}.")

    def view_appointments(self):
        for appointment in self.appointments:
            print(appointment)

