import uuid
import json
from main import AppointmentScheduler, Doctor, Patient, Appointment, DataManager

def generate_short_id():
    """Generate a short ID (11 characters)."""
    return str(uuid.uuid4())[:11]

class HospitalCLI:
    """A class to handle the command-line interface for the Hospital Appointment System."""
    
    def __init__(self, scheduler):
        # Initialize the scheduler and data manager
        self.scheduler = scheduler
        self.data_manager = DataManager()
        # Load data from JSON files when the program starts
        self.load_data()

    # --------------------------
    # Menu Display Methods
    # --------------------------
    def display_main_menu(self):
        """Display the main menu options."""
        print("\n--- Hospital Appointment System ---")
        print("1. Admin Area")
        print("2. User Area")
        print("3. Exit")

    def display_admin_menu(self):
        """Display the admin menu options."""
        print("\n--- Admin Area ---")
        print("1. Register Patient")
        print("2. Register Doctor")
        print("3. View All Appointments")
        print("4. Add Doctor Availability Slot")
        print("5. List registered Patients")
        print("6. List registered Doctors")
        print("7. Back to Main Menu")

    def display_user_menu(self):
        """Display the user menu options."""
        print("\n--- User Area ---")
        print("1. View My Appointments")
        print("2. Book Appointment")
        print("3. Cancel Appointment")
        print("4. Reschedule Appointment")
        print("5. Back to Main Menu")

    # --------------------------
    # Core Functionality
    # --------------------------
    def add_patient(self):
        """Add a new patient to the system and save to JSON."""
        print("\n--- Add Patient ---")
        # Collect patient details from user input
        name = input("Name: ").strip()
        contact_info = input("Contact Info: ").strip()
        age = int(input("Age: ").strip())
        gender = input("Gender: ").strip()
        card_no = input("Card Number: ").strip()
        dob = input("Date of Birth (YYYY-MM-DD): ").strip()
        specialization = input("Specialization of Doctor Needed: ").strip()

        # Create a new Patient object
        patient = Patient(name, contact_info, age, gender, card_no, dob, specialization)
        
        # Save patient data to JSON
        patient_data = {
            "name": name,
            "contact_info": contact_info,
            "age": age,
            "gender": gender,
            "card_no": card_no,
            "date_of_birth": dob,
            "Specialization of Doctor Needed": specialization,
            "patient_id": patient.person_id
        }
        
        try:
            # Append the new patient to the JSON file
            with open('patients.json', 'r+') as f:
                data = json.load(f)
                if any(p['patient_id'] == patient.person_id for p in data):
                    print("Error: Card number already exists!")
                    return
                data.append(patient_data)
                f.seek(0)
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            # Create a new JSON file if it doesn't exist
            with open('patients.json', 'w') as f:
                json.dump([patient_data], f, indent=4)
        
        # Add the patient to the scheduler
        self.scheduler.add_patient(patient)
        print(f"Patient added! ID: {patient.person_id}")
    
    def add_doctor(self):
        """Add a new doctor to the system."""
        print("\n--- Add Doctor ---")
        # Collect doctor details from user input
        name = input("Name: ").strip()
        contact_info = input("Contact Info: ").strip()
        age = int(input("Age: ").strip())
        gender = input("Gender: ").strip()
        specialization = input("Specialization: ").strip()
        
        # Create a new Doctor object
        doctor = Doctor(name, contact_info, age, gender, specialization)
        # Add the doctor to the scheduler
        self.scheduler.add_doctor(doctor)
        print(f"Doctor added! ID: {doctor.person_id}")

    def add_doctor_slot(self):
        """Add an availability slot for a doctor."""
        print("\n--- Add Doctor Availability ---")
        # Get the doctor ID from user input
        doctor_id = input("Doctor ID: ").strip()
        # Find the doctor in the scheduler
        doctor = next((d for d in self.scheduler.doctors if d.person_id == doctor_id), None)
        
        if not doctor:
            print("Doctor not found!")
            return
        
        # Collect slot details from user input
        date = input("Date (YYYY-MM-DD): ").strip()
        time = input("Time (HH:MM AM/PM): ").strip()
        # Add the slot to the doctor's schedule
        doctor.add_available_slot(date, time)
        print("Slot added!")

    def list_patients(self):
        """List all patients in the system."""
        print("\n--- Patients List ---")
        # Print each patient's ID and name
        for patient in self.scheduler.patients:
            print(f"ID: {patient.person_id} | Name: {patient.name} | Specialization of doctor needed: {patient.required_specialization}")

    def list_doctors(self):
        """List all doctors in the system."""
        print("\n --- Doctors List ---")
        # Print each doctor's ID, name, and specialization
        for doctor in self.scheduler.doctors:
            print(f" ID: {doctor.person_id} | Name: Dr. {doctor.name} | Specialization: {doctor.specialization}")
    def view_appointments(self):
        """View all appointments in the system."""
        print("\n--- All Appointments ---")
        # Display all appointments using the scheduler
        self.scheduler.view_appointments()

    def view_my_appointments(self, patient_id):
        """View appointments for a specific patient."""
        print("\n--- Your Appointments ---")
        # Filter appointments for the given patient ID
        appointments = [a for a in self.scheduler.appointments 
                        if a.patient.person_id == patient_id]
        # Print each appointment
        for appt in appointments:
            print(appt)

    def book_appointment(self, patient_id):
        """Book an appointment for a patient."""
        print("\n--- Book Appointment ---")
        
        # Find the patient by ID
        patient = next((p for p in self.scheduler.patients if p.person_id == patient_id), None)
        
        if not patient:
            print("Patient not found! Please check the patient ID.")
            return
        
        # Get available slots for the required specialization
        doctors = self.scheduler.find_doctors_by_specialization(patient.required_specialization)
        available_slots = []
        
        # Collect all available slots from matching doctors
        for doctor in doctors:
            for slot in doctor.get_schedule():
                available_slots.append((doctor, slot))
                print(f"{len(available_slots)}. Dr. {doctor.name} | {slot['date']} {slot['time']}")

        if not available_slots:
            print("No available slots!")
            return

        try:
            # Let the user choose a slot
            choice = int(input("Choose slot: ")) - 1
            doctor, slot = available_slots[choice]
            
            # Create and book the appointment
            appointment = Appointment(patient, doctor, slot['date'], slot['time'])
            self.scheduler.appointments.append(appointment)
            doctor.remove_slot(slot['date'], slot['time'])
            patient.appointments.append({
                'date': slot['date'],
                'time': slot['time'],
                'doctor': doctor.name
            })
            print("Appointment booked!")
        except (ValueError, IndexError):
            print("Invalid selection!")

    def cancel_appointment(self, patient_id):
        """Cancel an appointment for a patient."""
        print("\n--- Cancel Appointment ---")
        # Find cancellable appointments for the patient
        appointments = [a for a in self.scheduler.appointments 
                        if a.patient.person_id == patient_id 
                        and a.status == "Scheduled"]
        
        if not appointments:
            print("No cancellable appointments!")
            return
            
        # Display cancellable appointments
        for idx, appt in enumerate(appointments):
            print(f"{idx+1}. [ID: {appt.appointment_id}] {appt.date} {appt.time}")
        
        try:
            # Let the user choose an appointment to cancel
            choice = int(input("Select appointment: ")) - 1
            appt = appointments[choice]
            # Cancel the appointment
            self.scheduler.cancel_appointment(appt.appointment_id)
            print("Appointment cancelled!")
        except (ValueError, IndexError):
            print("Invalid selection!")

    def reschedule_appointment(self, patient_id):
        """Reschedule an appointment for a patient."""
        print("\n--- Reschedule Appointment ---")
        # Find reschedulable appointments for the patient
        appointments = [a for a in self.scheduler.appointments 
                        if a.patient.person_id == patient_id 
                        and a.status == "Scheduled"]
        
        if not appointments:
            print("No reschedulable appointments!")
            return
            
        # Display reschedulable appointments
        for idx, appt in enumerate(appointments):
            print(f"{idx+1}. [ID: {appt.appointment_id}] {appt.date} {appt.time}")
        
        try:
            # Let the user choose an appointment to reschedule
            choice = int(input("Select appointment: ")) - 1
            appt = appointments[choice]
            
            # Collect new date and time from user input
            new_date = input("New date (YYYY-MM-DD): ").strip()
            new_time = input("New time (HH:MM AM/PM): ").strip()

            # Get the doctor's available slots 
            doctor  = appt.doctor
            available_slots = doctor.get_schedule()

            # Check if the new slot is available
            if {"date": new_date, "time": new_time} in available_slots:
                success = self.scheduler.reschedule_appointment(appt.appointment_id, new_date, new_time)

                if success:
                    print("\nDoctor Approved: Reschduled Successfully!")
                else:
                    print("\nDoctor Denied: Unexpected error occurred!")
            else:
                print(f"\nDoctor declines: Dr. {doctor.name} is not availabe at {new_date} {new_time}")
                print("Please choose from available slots:")
                for slot in available_slots:
                    print(f" - {slot['date']} {slot['time']}")
        
        except (ValueError, IndexError):
            print("Invalid Selection")

    # --------------------------
    # Navigation Flow
    # --------------------------
    def admin_area(self):
        """Handle the admin area menu."""
        while True:
            self.display_admin_menu()
            choice = input("Choose option: ").strip()
            
            if choice == "1": self.add_patient()
            elif choice == "2": self.add_doctor()
            elif choice == "3": self.view_appointments()
            elif choice == "4": self.add_doctor_slot()
            elif choice == "5": self.list_patients()
            elif choice == "6": self.list_doctors()
            elif choice == "7": break
            else: print("Invalid choice!")

    def user_area(self):
        """Handle the user area menu."""
        while True:
            patient_id = input("\nEnter Patient ID: ").strip()
            
            # Load patient data from JSON file
            try:
                with open('patients.json', 'r') as f:
                    patients_data = json.load(f)
            except FileNotFoundError:
                print("Patient database not found! Please contact the administrator.")
                return
            except json.JSONDecodeError:
                print("Patient database is corrupted! Please contact the administrator.")
                return

            # Find the patient in the JSON data
            patient_data = next((p for p in patients_data if p['patient_id'] == patient_id), None)
            
            if not patient_data:
                print("Patient not found! Please try again.")
                continue  # Allow the user to retry
            else:
                # Create a Patient object from the JSON data
                patient = Patient(
                    name=patient_data['name'],
                    contact_info=patient_data['contact_info'],
                    age=patient_data['age'],
                    gender=patient_data['gender'],
                    card_no=patient_data['card_no'],
                    date_of_birth=patient_data['date_of_birth'],
                    required_specialization=patient_data['Specialization of Doctor Needed']
                )
                patient.person_id = patient_data['patient_id']  # Set the patient ID
                break  # Exit the loop if patient is found

        while True:
            self.display_user_menu()
            choice = input("Choose option: ").strip()
            
            # Validate menu choice
            if choice == "1":
                self.view_my_appointments(patient.person_id)
            elif choice == "2":
                self.book_appointment(patient.person_id)
            elif choice == "3":
                self.cancel_appointment(patient.person_id)
            elif choice == "4":
                self.reschedule_appointment(patient.person_id)
            elif choice == "5":
                print("Returning to the main menu.")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")
    
    def load_data(self):
        """
        Load data (patients, doctors, appointments) from JSON files.
        """
        self.scheduler.patients = DataManager.load_patients_from_json()
        self.scheduler.doctors = DataManager.load_doctors_from_json()
        self.scheduler.appointments = DataManager.load_appointments_from_json(
            self.scheduler.patients, self.scheduler.doctors
        )

    def save_data(self):
        """
        Save data (patients, doctors, appointments) to JSON files.
        """
        DataManager.save_patients_to_json(self.scheduler.patients)
        DataManager.save_doctors_to_json(self.scheduler.doctors)
        DataManager.save_appointments_to_json(self.scheduler.appointments)

    def run(self):
        """Run the hospital appointment system."""
        try:
            while True:
                self.display_main_menu()
                choice = input("Choose option: ").strip()
                
                if choice == "1": self.admin_area()
                elif choice == "2": self.user_area()
                elif choice == "3": break
                else: print("Invalid choice!")
        finally:
            self.save_data()  # Save data when the program exits

if __name__ == "__main__":
    # Initialize the scheduler and CLI
    scheduler = AppointmentScheduler()
    cli = HospitalCLI(scheduler)
    cli.run()