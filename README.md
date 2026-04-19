# 🦷 Dental Clinic Management System

A full-stack **web-based Dental Clinic Management System** designed to streamline and digitize daily clinical operations. This platform enhances efficiency, organization, and patient care through a centralized system for managing appointments, records, treatments, and payments.

Built using **Django (Python)**, **PostgreSQL**, and modern web technologies, the system provides role-based access for **Doctors** and **Receptionists**, ensuring smooth workflow and secure data handling.

---

## 🚀 Introduction

In today’s fast-paced healthcare environment, efficient management of dental clinics is essential. This system provides a **centralized digital solution** to manage all clinic activities including patient records, appointments, treatments, and billing.

The application improves communication between staff and patients while reducing manual work and errors, resulting in a more **organized, efficient, and patient-focused experience**.

---

## 👥 User Roles

### 👨‍💼 Receptionist (Admin)

* Manage doctors and schedules
* Register and manage patients
* Book and track appointments
* Handle payments and billing
* View reports and analytics

### 👨‍⚕️ Doctor

* View patient details
* Add diagnosis and treatment plans
* Upload X-ray images
* Prescribe medicines
* Access patient history and reports

---

## ✨ Key Features

* 📅 Appointment Scheduling System
* 🧾 Patient Registration & Records Management
* 🦷 Dental Chart & Diagnosis Tracking
* 🖼️ X-ray Image Upload & Management
* 💊 Medicine Prescription with Print Option
* 🧪 Lab Orders & Treatment Tracking
* 💰 Payment Management & Monthly Reports
* 📊 Analytics Dashboard
* 🔐 Role-Based Authentication System

---

## 🛠️ Tech Stack

**Frontend**

* HTML5
* CSS3
* JavaScript

**Backend**

* Python
* Django Framework

**Database**

* PostgreSQL

---

## ⚙️ Methodology

* **Software Development Model:** Prototype Model
* Iterative development approach for continuous improvement
* User feedback-driven enhancements

---

## 💻 Platform Requirements

* **Operating System:** Windows 10+ / Ubuntu 20.04+
* **Browser:** Google Chrome, Mozilla Firefox, or modern browsers
* **Backend:** Python with Django
* **Database:** PostgreSQL

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/dental-clinic-management-system.git
cd dental-clinic-management-system
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Database

* Install PostgreSQL
* Create a database
* Update database credentials in `settings.py`

---

### 5️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Run Server

```bash
python manage.py runserver
```

Open in browser:
http://127.0.0.1:8000/

---

## 📁 Project Structure

```
dental-clinic-management-system/
│
├── manage.py
├── project/
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── templates/
├── static/
│
├── requirements.txt
└── README.md
```

---

## 📸 Screenshots


<img width="932" height="424" alt="image" src="https://github.com/user-attachments/assets/8b49600a-86ee-450f-aa99-75d9a535105c" />
<img width="936" height="698" alt="image" src="https://github.com/user-attachments/assets/dc6a81d4-8560-40c2-9fca-b4e79d450e1e" />
<img width="935" height="432" alt="image" src="https://github.com/user-attachments/assets/7687e4f8-25d2-43ce-9beb-e91bfabb0fab" />
<img width="926" height="429" alt="image" src="https://github.com/user-attachments/assets/e64917a0-d814-4c87-a8c0-6acb4e683052" />
<img width="928" height="433" alt="image" src="https://github.com/user-attachments/assets/5ce6b922-d83d-4869-828b-0a819e7ff791" />
<img width="923" height="449" alt="image" src="https://github.com/user-attachments/assets/0b440dae-a178-48d4-8313-988fbdeed9a4" />
<img width="926" height="673" alt="image" src="https://github.com/user-attachments/assets/176021d4-6da4-4a30-98fb-122828453cae" />
<img width="929" height="423" alt="image" src="https://github.com/user-attachments/assets/eaf31fc7-ef4a-495c-b6a4-7e90e3ee9ae3" />
<img width="925" height="422" alt="image" src="https://github.com/user-attachments/assets/eb1ecf1d-78b2-49d7-a577-83714757dae6" />
<img width="929" height="426" alt="image" src="https://github.com/user-attachments/assets/7bfde786-d833-462c-bfb2-d759bee50ce1" />
<img width="933" height="429" alt="image" src="https://github.com/user-attachments/assets/5e06ea53-b59e-4ab0-ab93-56d3a16a54f1" />
<img width="928" height="425" alt="image" src="https://github.com/user-attachments/assets/5f692193-915f-4e6e-85fe-6ab84f1da85b" />


---

## 🔧 Troubleshooting

**Database Errors**

* Ensure PostgreSQL is running
* Verify credentials in `settings.py`

**Migration Issues**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Static Files Not Loading**

```bash
python manage.py collectstatic
```

---

## 🌟 Future Enhancements

* 🌐 Online Deployment (Cloud Hosting)
* 📱 Mobile Responsive UI
* 🔔 SMS/Email Notifications
* 📊 Advanced Analytics & Reports

---

## 👨‍💻 Author

**Shelva Ganesan M P**
🎓 MCA Student
💻 Web Developer

---

## ⭐ Support

If you find this project useful, please ⭐ star the repository on GitHub!
