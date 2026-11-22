#!/usr/bin/env python3
"""
seed_firestore.py — Seed all initial data into Firestore for NSS MVGR Portal.
Run once after setting up your Firebase project.

Usage:
    cd /Users/uppalapatinikhilvarma/nss-webapp
    python3 seed_firestore.py
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import firebase_admin
from firebase_admin import credentials, firestore

service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON', '').strip()
service_account_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT_PATH', '').strip()

if service_account_json:
    cred = credentials.Certificate(json.loads(service_account_json))
elif service_account_path:
    cred = credentials.Certificate(service_account_path)
else:
    raise RuntimeError("Set FIREBASE_SERVICE_ACCOUNT_JSON or FIREBASE_SERVICE_ACCOUNT_PATH in .env")

firebase_admin.initialize_app(cred)
db = firestore.client()

def seed_collection(collection_name, documents, id_field, doc_id_fn):
    """Seed documents and update the _counters entry."""
    for doc in documents:
        db.collection(collection_name).document(doc_id_fn(doc)).set(doc)
        print(f"  ✔ {collection_name}/{doc_id_fn(doc)}")
    max_id = max(d[id_field] for d in documents) if documents else 0
    db.collection('_counters').document(collection_name).set({'next_id': max_id + 1})
    print(f"  ✔ _counters/{collection_name} → next_id={max_id + 1}")

# ── Faculty Members ─────────────────────────────────────────────────────────
print("\n── Seeding faculty_members ──")
faculty_data = [
    {'id': 1, 'faculty_id': 'FAC001', 'username': 'dr_srao', 'name': 'Dr. S. Rao',
     'department': 'Computer Science & Engineering', 'email': 'srao@mvgrce.edu.in',
     'phone': '', 'password': 'nss@admin2026', 'role': 'NSS Faculty Coordinator'},
    {'id': 2, 'faculty_id': 'FAC002', 'username': 'prof_sharma', 'name': 'Prof. K. Sharma',
     'department': 'Electronics & Communication', 'email': 'ksharma@mvgrce.edu.in',
     'phone': '', 'password': 'nss@admin2026', 'role': 'NSS Faculty Coordinator'},
    {'id': 3, 'faculty_id': 'FAC003', 'username': 'dr_reddy', 'name': 'Dr. P. Reddy',
     'department': 'Mechanical Engineering', 'email': 'preddy@mvgrce.edu.in',
     'phone': '', 'password': 'nss@admin2026', 'role': 'NSS Faculty Coordinator'},
    {'id': 4, 'faculty_id': 'FAC004', 'username': 'dr_varma', 'name': 'Dr. M. Varma',
     'department': 'Chemical Engineering', 'email': 'mvarma@mvgrce.edu.in',
     'phone': '', 'password': 'nss@admin2026', 'role': 'NSS Faculty Coordinator'},
    {'id': 5, 'faculty_id': 'FAC005', 'username': 'prof_anand', 'name': 'Prof. T. Anand',
     'department': 'Information Engineering & Communication Technology (IE&CT)',
     'email': 'tanand@mvgrce.edu.in', 'phone': '', 'password': 'nss@admin2026',
     'role': 'NSS Faculty Coordinator'},
    {'id': 6, 'faculty_id': 'FAC006', 'username': 'dr_bhavani', 'name': 'Dr. V. Bhavani',
     'department': 'Data Engineering (DE)', 'email': 'vbhavani@mvgrce.edu.in',
     'phone': '', 'password': 'nss@admin2026', 'role': 'NSS Faculty Coordinator'},
]
seed_collection('faculty_members', faculty_data, 'id', lambda d: d['faculty_id'].upper())

# ── Volunteers ──────────────────────────────────────────────────────────────
print("\n── Seeding volunteers ──")
volunteer_data = [
    {'id': 1, 'roll_no': '21331A0501', 'name': 'Uppalapati Nikhil Varma',
     'email': 'nikhilvarma@mvgrce.edu.in', 'phone': '9876543210', 'password': 'password123',
     'branch': 'CSE', 'year': '3rd Year', 'blood_group': 'O+', 'address': 'MVGR Campus, Vizianagaram',
     'joined_date': '2026-01-10', 'hours': 48, 'hours_completed': 48, 'status': 'active'},
    {'id': 2, 'roll_no': '21331A0402', 'name': 'K. Sai Priya',
     'email': 'saipriya@mvgrce.edu.in', 'phone': '9876543211', 'password': 'password123',
     'branch': 'ECE', 'year': '3rd Year', 'blood_group': 'B+', 'address': 'Vizianagaram',
     'joined_date': '2026-01-15', 'hours': 36, 'hours_completed': 36, 'status': 'active'},
    {'id': 3, 'roll_no': '22331A0520', 'name': 'M. Rajesh',
     'email': 'rajesh.m@mvgrce.edu.in', 'phone': '9876543212', 'password': 'password123',
     'branch': 'CSE', 'year': '2nd Year', 'blood_group': 'A+', 'address': 'Vizianagaram',
     'joined_date': '2026-02-01', 'hours': 24, 'hours_completed': 24, 'status': 'active'},
    {'id': 4, 'roll_no': '22331A0801', 'name': 'A. Haritha',
     'email': 'haritha.a@mvgrce.edu.in', 'phone': '9876543213', 'password': 'password123',
     'branch': 'CHEM', 'year': '2nd Year', 'blood_group': 'A+', 'address': 'Vizianagaram',
     'joined_date': '2026-02-10', 'hours': 18, 'hours_completed': 18, 'status': 'active'},
    {'id': 5, 'roll_no': '22331A1201', 'name': 'V. Sneha',
     'email': 'sneha.v@mvgrce.edu.in', 'phone': '9876543214', 'password': 'password123',
     'branch': 'IE&CT', 'year': '3rd Year', 'blood_group': 'B+', 'address': 'Vizianagaram',
     'joined_date': '2026-01-20', 'hours': 32, 'hours_completed': 32, 'status': 'active'},
    {'id': 6, 'roll_no': '22331A5401', 'name': 'B. Tarun',
     'email': 'tarun.b@mvgrce.edu.in', 'phone': '9876543215', 'password': 'password123',
     'branch': 'DE', 'year': '2nd Year', 'blood_group': 'O+', 'address': 'Vizianagaram',
     'joined_date': '2026-02-15', 'hours': 20, 'hours_completed': 20, 'status': 'active'},
    {'id': 7, 'roll_no': '21331A0105', 'name': 'R. Manoj Kumar',
     'email': 'manoj.r@mvgrce.edu.in', 'phone': '9876543216', 'password': 'password123',
     'branch': 'CIVIL', 'year': '3rd Year', 'blood_group': 'AB+', 'address': 'Vizianagaram',
     'joined_date': '2026-01-12', 'hours': 28, 'hours_completed': 28, 'status': 'active'},
    {'id': 8, 'roll_no': '21331A0210', 'name': 'Ch. Divya',
     'email': 'divya.ch@mvgrce.edu.in', 'phone': '9876543217', 'password': 'password123',
     'branch': 'EEE', 'year': '3rd Year', 'blood_group': 'O+', 'address': 'Vizianagaram',
     'joined_date': '2026-01-18', 'hours': 30, 'hours_completed': 30, 'status': 'active'},
    {'id': 9, 'roll_no': '21331A0315', 'name': 'G. Suresh',
     'email': 'suresh.g@mvgrce.edu.in', 'phone': '9876543218', 'password': 'password123',
     'branch': 'MECH', 'year': '4th Year', 'blood_group': 'B+', 'address': 'Vizianagaram',
     'joined_date': '2026-01-08', 'hours': 42, 'hours_completed': 42, 'status': 'active'},
]
seed_collection('volunteers', volunteer_data, 'id', lambda d: d['roll_no'].upper())

# ── Events ──────────────────────────────────────────────────────────────────
print("\n── Seeding events ──")
event_data = [
    {'id': 1, 'title': 'Green Campus Mega Tree Plantation Drive', 'date': '2026-11-15',
     'time': '09:00 AM', 'venue': 'MVGR College Campus & Surroundings',
     'description': 'Annual tree plantation drive aimed at planting 500+ indigenous saplings across the campus and neighboring villages.',
     'category': 'environment', 'hours': 6, 'status': 'upcoming', 'organizer': 'NSS Unit MVGR',
     'max_volunteers': 100, 'registered_volunteers': ['21331A0501', '21331A0402']},
    {'id': 2, 'title': 'Voluntary Blood Donation Camp', 'date': '2026-11-25',
     'time': '10:00 AM', 'venue': 'Auditorium Block, MVGR',
     'description': 'Organized in association with Rotary Blood Bank and District Hospital. Each donor receives a certificate and refreshments.',
     'category': 'health', 'hours': 8, 'status': 'upcoming', 'organizer': 'NSS Red Ribbon Club',
     'max_volunteers': 80, 'registered_volunteers': ['21331A0501']},
    {'id': 3, 'title': 'Swachh Bharat Cleanliness & Awareness Drive', 'date': '2026-10-18',
     'time': '08:30 AM', 'venue': 'Boggula Dibba & Chintalavalasa Village',
     'description': 'Community awareness on waste segregation, single-use plastic ban, and public hygiene.',
     'category': 'cleanliness', 'hours': 10, 'status': 'completed', 'organizer': 'NSS Unit MVGR',
     'max_volunteers': 60, 'registered_volunteers': ['21331A0501', '21331A0402', '22331A0520']},
    {'id': 4, 'title': 'Digital Literacy Workshop for Rural High Schools', 'date': '2026-10-05',
     'time': '10:00 AM', 'venue': 'Z.P. High School, Denkada',
     'description': 'Volunteers conducted hands-on computer sessions and cyber safety awareness for 9th and 10th standard students.',
     'category': 'education', 'hours': 8, 'status': 'completed', 'organizer': 'NSS Tech Wing',
     'max_volunteers': 40, 'registered_volunteers': ['21331A0501']},
]
seed_collection('events', event_data, 'id', lambda d: str(d['id']))

# ── Attendance Records ───────────────────────────────────────────────────────
print("\n── Seeding attendance_records ──")
attendance_data = [
    {'id': 1, 'event_id': 3, 'event_title': 'Swachh Bharat Cleanliness & Awareness Drive',
     'date': '2026-10-18', 'present': ['21331A0501', '21331A0402', '22331A0520'], 'hours': 10},
    {'id': 2, 'event_id': 4, 'event_title': 'Digital Literacy Workshop for Rural High Schools',
     'date': '2026-10-05', 'present': ['21331A0501'], 'hours': 8},
]
seed_collection('attendance_records', attendance_data, 'id', lambda d: str(d['id']))

# ── News Items ───────────────────────────────────────────────────────────────
print("\n── Seeding news_items ──")
news_data = [
    {'id': 1, 'title': '57th National Service Scheme (NSS) Foundation Day Celebrated',
     'date': '2026-09-24',
     'content': "MVGRCE(A) celebrated NSS Foundation Day on 24th September 2026 with an inspiring commemorative rally and cultural assembly celebrating the motto 'Not Me But You', honoring student volunteer excellence.",
     'category': 'announcement', 'published_by': 'NSS Unit MVGR', 'department': 'All Departments'},
    {'id': 2, 'title': 'Annual Special Rural Camp 2026 - Registrations Concluded',
     'date': '2026-10-01',
     'content': 'Registrations for the prestigious 7-Day Residential Annual Special Camp closed on 15th October 2026 following overwhelming student interest.',
     'category': 'event', 'published_by': 'NSS Unit MVGR', 'department': 'All Departments'},
    {'id': 3, 'title': 'Mega Voluntary Blood Donation Camp Scheduled for 25th November',
     'date': '2026-10-15',
     'content': 'MVGR NSS Red Ribbon Club, in joint collaboration with Rotary Blood Bank and Vizianagaram District Hospital, has finalized arrangements for the upcoming Voluntary Blood Donation Camp on 25th November 2026.',
     'category': 'activity', 'published_by': 'Red Ribbon Club', 'department': 'All Departments'},
    {'id': 4, 'title': 'Swachh Bharat Cleanliness & Awareness Drive Successfully Conducted',
     'date': '2026-10-18',
     'content': 'Over 60 dedicated NSS student volunteers successfully concluded a full-day community cleanliness and plastic-waste awareness campaign across Boggula Dibba and Chintalavalasa village on 18th October 2026.',
     'category': 'activity', 'published_by': 'NSS Unit MVGR', 'department': 'All Departments'},
    {'id': 5, 'title': 'Green Campus Mega Tree Plantation Drive Announced',
     'date': '2026-11-02',
     'content': 'MVGR NSS Cell has scheduled the Green Campus Mega Tree Plantation Drive for 15th November 2026 across the campus and neighboring adopted villages. Over 500 indigenous saplings have been procured.',
     'category': 'announcement', 'published_by': 'NSS Unit MVGR', 'department': 'All Departments'},
]
seed_collection('news_items', news_data, 'id', lambda d: str(d['id']))

# ── Audit Logs ───────────────────────────────────────────────────────────────
print("\n── Seeding audit_logs ──")
audit_data = [
    {'id': 1, 'faculty_name': 'Dr. S. Rao', 'faculty_id': 'FAC001', 'department': 'CSE',
     'action_type': 'Marked Attendance',
     'description': 'Recorded attendance for 3 volunteers in "Swachh Bharat Cleanliness & Awareness Drive" (+10 hrs credit each)',
     'target': 'Swachh Bharat Cleanliness & Awareness Drive',
     'timestamp': '2026-10-18 11:30 AM', 'badge_class': 'badge-attendance'},
    {'id': 2, 'faculty_name': 'Prof. K. Sharma', 'faculty_id': 'FAC002', 'department': 'ECE',
     'action_type': 'Added Event',
     'description': 'Created new campus drive: "Voluntary Blood Donation Camp" (8 credit hours, 80 quota)',
     'target': 'Voluntary Blood Donation Camp',
     'timestamp': '2026-10-20 03:15 PM', 'badge_class': 'badge-event'},
    {'id': 3, 'faculty_name': 'Dr. S. Rao', 'faculty_id': 'FAC001', 'department': 'CSE',
     'action_type': 'Published News',
     'description': 'Published circular: "Annual Special Camp Registration Open" for 7-day residential camp',
     'target': 'Annual Special Camp Registration Open',
     'timestamp': '2026-10-22 09:45 AM', 'badge_class': 'badge-news'},
    {'id': 4, 'faculty_name': 'Dr. P. Reddy', 'faculty_id': 'FAC003', 'department': 'MECH',
     'action_type': 'Approved Hours',
     'description': 'Approved 8 service credit hours for volunteer Uppalapati Nikhil Varma in Digital Literacy Workshop',
     'target': 'Digital Literacy Workshop',
     'timestamp': '2026-10-25 04:00 PM', 'badge_class': 'badge-approval'},
]
seed_collection('audit_logs', audit_data, 'id', lambda d: str(d['id']))

print("\n✅ All collections seeded successfully into Firebase Firestore!")
print("   Project: nss-webapp")
print("   Collections: faculty_members, volunteers, events, attendance_records, news_items, audit_logs")
