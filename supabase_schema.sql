-- ====================================================================
-- MVGR NSS Portal - Supabase Database Schema & Initial Seed
-- Run this in the Supabase Dashboard -> SQL Editor -> New Query
-- ====================================================================

-- 1. Faculty Coordinators Table
CREATE TABLE IF NOT EXISTS faculty_members (
    id SERIAL PRIMARY KEY,
    faculty_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    department VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) DEFAULT '',
    password VARCHAR(255) NOT NULL,
    role VARCHAR(100) DEFAULT 'NSS Faculty Coordinator',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Volunteers (Students) Table
CREATE TABLE IF NOT EXISTS volunteers (
    id SERIAL PRIMARY KEY,
    roll_no VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    branch VARCHAR(100) NOT NULL,
    year VARCHAR(50) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    address TEXT DEFAULT 'MVGR Campus, Vizianagaram',
    joined_date VARCHAR(20) DEFAULT CURRENT_DATE::text,
    hours INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Events Table
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date VARCHAR(20) NOT NULL,
    time VARCHAR(50) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    hours INTEGER DEFAULT 5,
    status VARCHAR(50) DEFAULT 'upcoming',
    organizer VARCHAR(100) DEFAULT 'NSS Unit MVGR',
    max_volunteers INTEGER DEFAULT 50,
    registered_volunteers TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Attendance Records Table
CREATE TABLE IF NOT EXISTS attendance_records (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    event_title VARCHAR(255) NOT NULL,
    date VARCHAR(20) NOT NULL,
    present TEXT[] DEFAULT '{}',
    hours INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. News / Circulars Table
CREATE TABLE IF NOT EXISTS news_items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'announcement',
    published_by VARCHAR(150) DEFAULT 'NSS Unit MVGR',
    department VARCHAR(150) DEFAULT 'All Departments',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Audit Logs Table (Contributions)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    faculty_name VARCHAR(150) NOT NULL,
    faculty_id VARCHAR(50) NOT NULL,
    department VARCHAR(150) NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    target VARCHAR(255) DEFAULT '',
    timestamp VARCHAR(50) NOT NULL,
    badge_class VARCHAR(50) DEFAULT 'badge-event',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Contact Inquiries Table
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ====================================================================
-- SEED INITIAL DATA
-- ====================================================================

-- Seed Faculty
INSERT INTO faculty_members (faculty_id, username, name, department, email, password, role)
VALUES
    ('FAC001', 'dr_srao', 'Dr. S. Rao', 'Computer Science & Engineering', 'srao@mvgrce.edu.in', 'nss@admin2026', 'NSS Faculty Coordinator'),
    ('FAC002', 'prof_ksharma', 'Prof. K. Sharma', 'Electronics & Communication Engineering', 'ksharma@mvgrce.edu.in', 'nss@admin2026', 'NSS Faculty Coordinator'),
    ('FAC003', 'dr_preddy', 'Dr. P. Reddy', 'Mechanical Engineering', 'preddy@mvgrce.edu.in', 'nss@admin2026', 'NSS Faculty Coordinator'),
    ('FAC004', 'dr_varma', 'Dr. M. Varma', 'Chemical Engineering', 'mvarma@mvgrce.edu.in', 'nss@admin2026', 'NSS Faculty Coordinator'),
    ('FAC005', 'prof_anand', 'Prof. T. Anand', 'Information Engineering & Communication Technology (IE&CT)', 'tanand@mvgrce.edu.in', 'nss@admin2026', 'NSS Faculty Coordinator'),
    ('FAC006', 'dr_bhavani', 'Dr. V. Bhavani', 'Data Engineering (DE)', 'vbhavani@mvgrce.edu.in', 'nss@admin2026', 'NSS Faculty Coordinator')
ON CONFLICT (faculty_id) DO NOTHING;

-- Seed Sample Volunteers
INSERT INTO volunteers (roll_no, name, email, phone, password, branch, year, blood_group, hours, status, joined_date)
VALUES
    ('21331A0501', 'Uppalapati Nikhil Varma', 'nikhilvarma@mvgrce.edu.in', '9876543210', 'password123', 'CSE', '3rd Year', 'O+', 45, 'active', '2026-01-10'),
    ('21331A0402', 'B. Sai Kumar', 'saikumar@mvgrce.edu.in', '9876543211', 'password123', 'ECE', '3rd Year', 'A+', 38, 'active', '2026-01-12'),
    ('22331A0520', 'Ch. Lakshmi', 'lakshmi@mvgrce.edu.in', '9876543212', 'password123', 'CSE', '2nd Year', 'B+', 24, 'active', '2026-02-01')
ON CONFLICT (roll_no) DO NOTHING;

-- Seed Sample Events
INSERT INTO events (title, date, time, venue, description, category, hours, status, organizer, max_volunteers, registered_volunteers)
VALUES
    ('Mega Tree Plantation Drive 2026', '2026-11-20', '09:00 AM', 'MVGR Campus & Surrounding Villages', 'Annual tree plantation drive targeting 500 saplings in and around campus premises.', 'environment', 6, 'upcoming', 'NSS Unit MVGR', 50, ARRAY['21331A0501', '21331A0402']),
    ('Voluntary Blood Donation Camp', '2026-11-28', '10:00 AM', 'Main Auditorium, MVGRCE', 'In association with Rotary Blood Bank Vizianagaram. Blood donation by students and faculty.', 'health', 8, 'upcoming', 'Red Ribbon Club & NSS', 80, ARRAY['21331A0501']),
    ('Swachh Bharat Cleanliness & Awareness Drive', '2026-10-18', '08:00 AM', 'Boggula Dibba & Chintalavalasa Village', 'Community awareness on waste segregation, single-use plastic ban, and public hygiene.', 'cleanliness', 10, 'completed', 'NSS Unit MVGR', 60, ARRAY['21331A0501', '21331A0402', '22331A0520']),
    ('Digital Literacy Workshop for Rural High Schools', '2026-10-05', '10:00 AM', 'Z.P. High School, Denkada', 'Volunteers conducted hands-on computer sessions and cyber safety awareness for 9th and 10th standard students.', 'education', 8, 'completed', 'NSS Tech Wing', 40, ARRAY['21331A0501'])
ON CONFLICT DO NOTHING;

-- Seed News / Circulars
INSERT INTO news_items (title, date, content, category, published_by, department)
VALUES
    ('NSS Day Celebration - 24th September', '2026-09-24', 'NSS Day is celebrated on 24th September every year to commemorate the founding of NSS. Join us for special events and community service activities.', 'announcement', 'NSS Program Officer', 'All Departments'),
    ('Annual Special Camp Registration Open', '2026-10-01', 'Registration for the Annual Special Camp (7-day residential camp) is now open. Last date to register is 15th October.', 'event', 'NSS Unit MVGR', 'All Departments'),
    ('Blood Donation Drive - Join Us!', '2026-10-15', 'NSS Unit is organizing a blood donation drive in collaboration with the local hospital. All healthy volunteers are encouraged to participate.', 'activity', 'Red Ribbon Club', 'All Departments')
ON CONFLICT DO NOTHING;
