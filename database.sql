-- MINDCARE Database Schema
CREATE DATABASE IF NOT EXISTS psychcure_db;
USE psychcure_db;

-- 1. Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_image_url VARCHAR(255) DEFAULT 'default_profile.jpg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    college_email VARCHAR(100) UNIQUE NOT NULL,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(100),
    year VARCHAR(20),
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    profile_image_url VARCHAR(255) DEFAULT 'default_profile.jpg',
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Counselors Table
CREATE TABLE IF NOT EXISTS counselors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    faculty_id VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    specialization VARCHAR(100),
    password VARCHAR(255) NOT NULL,
    profile_image_url VARCHAR(255) DEFAULT 'default_profile.jpg',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Check-ins Table
CREATE TABLE IF NOT EXISTS checkins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    mood VARCHAR(50) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 5. Lifestyle Table
CREATE TABLE IF NOT EXISTS lifestyle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    sleep_hours FLOAT,
    exercise_days INT,
    stress_level INT,
    mood_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 6. Sessions Table
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    counselor_id INT NOT NULL,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    reason TEXT,
    mode ENUM('online', 'offline') DEFAULT 'offline',
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (counselor_id) REFERENCES counselors(id) ON DELETE CASCADE
);

-- 7. Support Groups Table
CREATE TABLE IF NOT EXISTS support_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    counselor_id INT NOT NULL,
    tags VARCHAR(255),
    max_students INT DEFAULT 10,
    frequency VARCHAR(50),
    image_url VARCHAR(255) DEFAULT 'default_group.jpg',
    status ENUM('active', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (counselor_id) REFERENCES counselors(id) ON DELETE CASCADE
);

-- 8. Group Members Table
CREATE TABLE IF NOT EXISTS group_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    student_id INT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_membership (group_id, student_id),
    FOREIGN KEY (group_id) REFERENCES support_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 9. Session Notes Table (Detailed)
CREATE TABLE IF NOT EXISTS session_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    counselor_id INT NOT NULL,
    format ENUM('soap', 'dap', 'free') NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (counselor_id) REFERENCES counselors(id) ON DELETE CASCADE
);

-- 10. Risk Alerts Table
CREATE TABLE IF NOT EXISTS risk_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    risk_level ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    description TEXT,
    status ENUM('active', 'resolved') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 11. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_type ENUM('student', 'counselor', 'admin') NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Password Resets Table
CREATE TABLE IF NOT EXISTS password_resets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Exam Plans Table
CREATE TABLE IF NOT EXISTS exam_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    exam_date DATE NOT NULL,
    stress_level INT NOT NULL,
    subjects TEXT NOT NULL,
    preparation_level INT NOT NULL,
    stress_message TEXT,
    preparation_message TEXT,
    plan_message TEXT,
    subject_plan JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 14. Lifestyle Logs Table
CREATE TABLE IF NOT EXISTS lifestyle_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    sleep_hours FLOAT,
    bedtime VARCHAR(20),
    screen_time_before_sleep INT,
    activity_level VARCHAR(100),
    energy_level INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 15. Time Management Plans Table
CREATE TABLE IF NOT EXISTS time_management_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    classes_per_week INT NOT NULL,
    pending_assignments INT NOT NULL,
    study_hours_per_day FLOAT NOT NULL,
    sleep_hours_per_night FLOAT NOT NULL,
    workload_status VARCHAR(50),
    suggestions JSON,
    schedule JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Default Admin Account (password: admin123)
-- In a real app, use a hashed password. This is a placeholder for development.
INSERT IGNORE INTO admins (username, password) VALUES ('admin', 'admin123');

-- 16. Group Tasks Table
CREATE TABLE IF NOT EXISTS group_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    counselor_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    due_date VARCHAR(100),
    status VARCHAR(50) DEFAULT 'assigned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES support_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (counselor_id) REFERENCES counselors(id) ON DELETE CASCADE
);

-- 17. Task Submissions Table
CREATE TABLE IF NOT EXISTS task_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    student_id INT NOT NULL,
    submission_text TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'submitted',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES group_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 18. Group Announcements Table
CREATE TABLE IF NOT EXISTS group_announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    counselor_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES support_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (counselor_id) REFERENCES counselors(id) ON DELETE CASCADE
);

-- 19. Group Posts Table (For the Feed)
CREATE TABLE IF NOT EXISTS group_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    user_type ENUM('student', 'counselor') NOT NULL,
    content TEXT NOT NULL,
    is_pinned TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES support_groups(id) ON DELETE CASCADE
);

-- 20. Post Likes Table
CREATE TABLE IF NOT EXISTS post_likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    user_type ENUM('student', 'counselor') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_like (post_id, user_id, user_type),
    FOREIGN KEY (post_id) REFERENCES group_posts(id) ON DELETE CASCADE
);

-- 21. Post Comments Table
CREATE TABLE IF NOT EXISTS post_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    user_type ENUM('student', 'counselor') NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES group_posts(id) ON DELETE CASCADE
);

-- Counselor Working Hours
CREATE TABLE IF NOT EXISTS working_hours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    counselor_id INT NOT NULL,
    day_of_week VARCHAR(15) NOT NULL,
    start_time TIME DEFAULT '09:00:00',
    end_time TIME DEFAULT '17:00:00',
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (counselor_id) REFERENCES counselors(id) ON DELETE CASCADE,
    UNIQUE KEY (counselor_id, day_of_week)
);

-- Lifestyle Logs Table for detailed tracking
CREATE TABLE IF NOT EXISTS lifestyle_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    sleep_hours FLOAT,
    bedtime VARCHAR(50),
    screen_time_before_sleep INT,
    activity_level VARCHAR(50),
    energy_level INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
C R E A T E   T A B L E   I F   N O T   E X I S T S   s e s s i o n _ r e q u e s t s   ( 
         i d   I N T   A U T O _ I N C R E M E N T   P R I M A R Y   K E Y , 
         s t u d e n t _ i d   I N T   N O T   N U L L , 
         s e s s i o n _ i d   I N T   N O T   N U L L , 
         s t a t u s   E N U M ( ' p e n d i n g ' ,   ' a p p r o v e d ' ,   ' r e j e c t e d ' )   D E F A U L T   ' p e n d i n g ' , 
         c r e a t e d _ a t   T I M E S T A M P   D E F A U L T   C U R R E N T _ T I M E S T A M P , 
         F O R E I G N   K E Y   ( s t u d e n t _ i d )   R E F E R E N C E S   s t u d e n t s ( i d )   O N   D E L E T E   C A S C A D E , 
         F O R E I G N   K E Y   ( s e s s i o n _ i d )   R E F E R E N C E S   s e s s i o n s ( i d )   O N   D E L E T E   C A S C A D E 
 ) ;  
 