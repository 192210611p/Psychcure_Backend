# MINDCARE Backend Setup Instructions

This backend is built using **Flask (Python)** and connects to a **MySQL** database.

## Prerequisites
1. **XAMPP** (with MySQL/MariaDB running)
2. **Python 3.x** installed

## 1. Database Setup
1. Open **XAMPP Control Panel** and start **Apache** and **MySQL**.
2. Open your browser and go to `http://localhost/phpmyadmin/`.
3. Create a new database named `psychcure_db`.
4. Click on the `Import` tab and upload the `database.sql` file located in this folder.
5. Alternatively, run the SQL commands in the SQL tab.

## 2. Python Environment Setup
1. Open a terminal/command prompt in this directory (`c:\xampp\htdocs\psychcure`).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 3. Running the Backend
1. In the same terminal, run:
   ```bash
   python app.py
   ```
2. The server will start at `http://0.0.0.0:5000/`.
3. Make sure your computer's IP address (`172.29.206.34`) is correctly entered in the Android app's `NetworkClient.kt` file.

## 4. Default Accounts
- **Admin**: Username: `admin`, Password: `admin123`
- **Counselor**: Any email added by admin, Default Password fallback: `counselor123`

## Troubleshooting
- **CORS Errors**: Already handled in `app.py`.
- **Database Connection**: Ensure your MySQL settings match `db_config` in `app.py` (Default: host='localhost', user='root', password='').
