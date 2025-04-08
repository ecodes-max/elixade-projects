## **Hospital Appointment System Documentation**

**Table of Contents**
<b>
1. Introduction
2. System Overview
3. Architecture & Design Principles

4. Key Classes
    <ul>Person </ul>
    <ul>Doctor </ul>
    <ul>Patient </ul>
    <ul>Appointment </ul>
    <ul>AppointmentScheduler </ul>
    <ul>DataManager </ul>
    <ul>HospitalCLI</ul>
5. Data Persistence with JSON
6. How to Run the Program
7. User & Admin Areas
8. Future Enhancements
9. Conclusion
</b>

<h3> <b> 1. Introduction</b> </h3> 
<p> The Hospital Appointment System is a CLI-based scheduling application built using Python. It allows patients to book, view, cancel, and reschedule appointments with doctors. The system leverages object-oriented programming (OOP) principles for modularity, maintainability, and scalability. </p>


<h3> <b> 2. System Overview </h3> </b>
<ol> <b> Purpose: </ol> </b>
 To facilitate efficient scheduling between doctors and patients based on required specializations.

<ul> <b>Technologies Used: </ul></b>

<li>Python </li>
<li>JSON for data persistence </li>
<li> Command-Line Interface (CLI) for user interaction</li>

<ul> <b>Key Features: </ul> </b>

<li> Role-based access: Admin & User </li>
<li> Unique identification for all entities </li>
<li> Data storage and retrieval via JSON files </li>
<li> Core scheduling, cancellation, and rescheduling functionalities </li>


<h3> <b> 3. Architecture & Design Principles </h3> </b> 
The system is designed using OOP principles:

<li>Encapsulation:
Each class (e.g., Person) encapsulates its data and exposes public methods for interaction. </li>

<li> Abstraction:
High-level methods (e.g., schedule_appointment()) hide complex internal logic. </li>

<li> Inheritance:
Doctor and Patient classes inherit common properties from the base Person class. </li>


<h3> <b> 4. Key Classes </h3> </b> 

**Person**
- **Purpose:**  
  Base class for all entities in the system.
- **Key Attributes:**  
  - `name`, `contact_info`, `age`, `gender`
  - `person_id` (a unique identifier generated using `uuid`)
- **Key Methods:**  
  - Getters/Setters
  - `update_info()`
  - `__str__()` for a human-readable representation

### Doctor
- **Purpose:**  
  Represents a doctor.
- **Additional Attributes:**  
  - `specialization`
  - `schedule` (list of available slots)
- **Key Methods:**  
  - `add_available_slot(date, time)`
  - `remove_slot(date, time)`
  - `get_schedule()`

### Patient
- **Purpose:**  
  Represents a patient.
- **Additional Attributes:**  
  - `card_no`, `date_of_birth`, `required_specialization`
  - `appointments` (list of booked appointments)
- **Key Methods:**  
  - `add_appointment(date, time)`
  - `cancel_appointment(date, time)`

### Appointment
- **Purpose:**  
  Captures the details of an appointment.
- **Key Attributes:**  
  - `appointment_id`, `patient`, `doctor`, `date`, `time`, `status`
- **Key Methods:**  
  - `cancel_appointment()`
  - `reschedule_appointment(new_date, new_time)`
  - `__str__()` for detailed output

### AppointmentScheduler
- **Purpose:**  
  Manages overall scheduling.
- **Key Attributes:**  
  - Lists of `appointments`, `doctors`, and `patients`
- **Key Methods:**  
  - `add_doctor()`, `add_patient()`
  - `schedule_appointment(patient, date, time)`
  - `cancel_appointment(appointment_id)`
  - `view_appointments()`
  - `reschedule_appointment(appointment_id, new_date, new_time)`

### DataManager
- **Purpose:**  
  Handles loading and saving of data to JSON files.
- **Key Methods:**  
  - `load_patients_from_json()`, `save_patients_to_json()`
  - `load_doctors_from_json()`, `save_doctors_to_json()`
  - `load_appointments_from_json()`, `save_appointments_to_json()`

### HospitalCLI
- **Purpose:**  
  Provides the command-line interface.
- **Admin Area:**  
  - Add Patient, Add Doctor, View All Appointments, Add Doctor Availability Slot, List Patients, List D
- **User Area:**  
  - View My Appointments, Book Appointment, Cancel Appointment, Reschedule Appointment
- **Data Handling:**  
  - Loads data on startup and saves on exit

---

## 5. Data Persistence with JSON

- **Implementation:**  
  The `DataManager` class reads from and writes to JSON files (e.g., `patients.json`, `doctors.json`, `appointments.json`).
- **Benefits:**  
  - Data is human-readable and easily modifiable.
  - Ensures persistence of records between program executions.

---

## 6. How to Run the Program

1. **Prerequisites:**  
   - Python 3.x installed.
2. **Files in the Project:**  
   - `main.py`: Contains core classes and logic.
   - `HospitalCLI.py`: Contains the CLI implementation.
   - JSON files (`patients.json`, `doctors.json`, `appointments.json`) are created/updated automatically.
3. **Execution:**  
   - Open a terminal in the project directory.
   - Run the command:  
     ```
     python HospitalCLI.py
     ```
4. **Usage:**  
   - Follow the on-screen menus to navigate between Admin and User areas.

---

## 7. User & Admin Areas

- **Admin Area:**  
  - **Functions:**  
    - Add Patient, Add Doctor, View All Appointments, Add Doctor Availability Slot, List Patients.
  - **Access:**  
    - Select the Admin area from the main menu.
  
- **User Area:**  
  - **Functions:**  
    - View My Appointments, Book Appointment, Cancel Appointment, Reschedule Appointment.
  - **Access:**  
    - Enter your Patient ID to access your personal appointment management.

---

## 8. Future Enhancements

- **Graphical User Interface (GUI):**  
  Implement a GUI using frameworks like Tkinter or a web-based interface.
- **Database Integration:**  
  Replace JSON file storage with a relational database (e.g., SQLite, PostgreSQL).
- **Additional Features:**  
  - Email/SMS notifications
  - Advanced reporting and analytics

---

## 9. Conclusion

The Hospital Appointment System demonstrates a practical application of OOP principles in Python to solve real-world scheduling challenges. With clear separation of concerns, role-based access, and data persistence via JSON, the system is both scalable and maintainable. Future improvements can further enhance user experience and performance.

---
