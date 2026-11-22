# Firebase Firestore Schema — NSS Portal

This document describes the Firestore collections that replace the Supabase PostgreSQL tables, explains document structure, and provides a Python seed script for initial data population.

---

## Overview

| Firestore Collection    | Replaces Supabase Table   | Document ID Strategy                  |
|-------------------------|---------------------------|---------------------------------------|
| `volunteers`            | `volunteers`              | `roll_no` (uppercase string)          |
| `faculty_members`       | `faculty_members`         | `faculty_id` (uppercase string)       |
| `events`                | `events`                  | String of numeric id e.g. `"1"`       |
| `attendance_records`    | `attendance_records`      | String of numeric id e.g. `"1"`       |
| `news_items`            | `news_items`              | String of numeric id e.g. `"1"`       |
| `audit_logs`            | `audit_logs`              | String of numeric id e.g. `"1"`       |
| `contacts`              | `contacts`                | String of numeric id e.g. `"1"`       |
| `_counters`             | *(internal)*              | Collection name (tracks next auto-id) |

---

## Collection Schemas

### `volunteers`
```
Document ID: <ROLL_NO_UPPERCASE>  e.g. "22A91A05B4"

{
  id:           <int>         // numeric auto-increment
  roll_no:      <str>         // uppercase, used as doc ID
  name:         <str>
  email:        <str>
  phone:        <str>
  password:     <str>         // hashed or plaintext (app-managed)
  branch:       <str>         // e.g. "CSE"
  year:         <str>         // e.g. "2nd Year"
  blood_group:  <str>         // e.g. "O+"
  address:      <str>
  joined_date:  <str>         // "YYYY-MM-DD"
  hours:        <int>         // total NSS hours completed
  hours_completed: <int>      // alias kept in sync with hours
  status:       <str>         // "active" | "inactive"
}
```

### `faculty_members`
```
Document ID: <FACULTY_ID_UPPERCASE>  e.g. "FAC001"

{
  id:          <int>
  faculty_id:  <str>          // uppercase, used as doc ID
  username:    <str>
  name:        <str>
  department:  <str>
  email:       <str>
  phone:       <str>
  password:    <str>
  role:        <str>          // "admin" | "faculty"
}
```

### `events`
```
Document ID: "<numeric_id>"  e.g. "1"

{
  id:                    <int>
  title:                 <str>
  date:                  <str>   // "YYYY-MM-DD"
  time:                  <str>   // "HH:MM"
  venue:                 <str>
  description:           <str>
  category:              <str>
  hours:                 <int>   // NSS hours awarded for attending
  status:                <str>   // "upcoming" | "ongoing" | "completed"
  organizer:             <str>
  max_volunteers:        <int>
  registered_volunteers: [<str>] // list of roll_nos (uppercase)
}
```

### `attendance_records`
```
Document ID: "<numeric_id>"  e.g. "1"

{
  id:          <int>
  event_id:    <int>           // references events.id
  event_title: <str>
  date:        <str>           // "YYYY-MM-DD"
  present:     [<str>]         // list of roll_nos (uppercase)
  hours:       <int>
}
```
> Upsert is done by `event_id` — there is at most one attendance record per event.

### `news_items`
```
Document ID: "<numeric_id>"  e.g. "1"

{
  id:           <int>
  title:        <str>
  date:         <str>          // "YYYY-MM-DD"
  content:      <str>
  category:     <str>
  published_by: <str>
  department:   <str>
}
```

### `audit_logs`
```
Document ID: "<numeric_id>"  e.g. "1"

{
  id:           <int>
  faculty_name: <str>
  faculty_id:   <str>
  department:   <str>
  action_type:  <str>
  description:  <str>
  target:       <str>
  timestamp:    <str>          // ISO or human-readable datetime
  badge_class:  <str>          // CSS class for badge colour
}
```

### `contacts`
```
Document ID: "<numeric_id>"  e.g. "1"

{
  id:      <int>
  name:    <str>
  email:   <str>
  subject: <str>
  message: <str>
  date:    <str>              // "YYYY-MM-DD HH:MM"
}
```

### `_counters` (internal)
```
Document ID: <collection_name>  e.g. "events"

{
  next_id: <int>   // next value to assign; incremented on every insert
}
```

---

## Firestore Indexes Required

The following single-field indexes are created automatically by Firestore.  
The only **composite** index you may need is if you add ordering + filtering together in a future query. For the current `db.py` implementation, only single-field ordering is used (or Python-side sorting), so no manual composite indexes are needed.

---

## Python Seed Script

Run this once to populate initial/demo data into Firestore.

```python
#!/usr/bin/env python3
"""
seed_firestore.py — Seed initial data into Firestore for NSS Portal.

Usage:
    export FIREBASE_SERVICE_ACCOUNT_JSON='<json string>'
    # OR
    export FIREBASE_SERVICE_ACCOUNT_PATH='/path/to/serviceAccountKey.json'

    python3 seed_firestore.py
"""

import os
import json
from datetime import datetime

# ── Init Firebase ──────────────────────────────────────────────────────────
import firebase_admin
from firebase_admin import credentials, firestore

service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON', '').strip()
service_account_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT_PATH', '').strip()

if service_account_json:
    cred = credentials.Certificate(json.loads(service_account_json))
elif service_account_path:
    cred = credentials.Certificate(service_account_path)
else:
    raise RuntimeError("Set FIREBASE_SERVICE_ACCOUNT_JSON or FIREBASE_SERVICE_ACCOUNT_PATH")

firebase_admin.initialize_app(cred)
db = firestore.client()

# ── Helper ─────────────────────────────────────────────────────────────────
def seed_collection(collection_name, documents, id_field, doc_id_fn):
    """
    Seed documents into a Firestore collection and set the _counters entry.
    documents: list of dicts, each must have an integer `id` field.
    doc_id_fn: callable(doc) -> Firestore document ID string
    """
    for doc in documents:
        db.collection(collection_name).document(doc_id_fn(doc)).set(doc)
        print(f"  ✔ {collection_name}/{doc_id_fn(doc)}")
    max_id = max(d[id_field] for d in documents) if documents else 0
    db.collection('_counters').document(collection_name).set({'next_id': max_id + 1})
    print(f"  ✔ _counters/{collection_name} → next_id={max_id + 1}")

# ── Seed Data ──────────────────────────────────────────────────────────────
print("\n── Seeding faculty_members ──")
faculty_data = [
    {
        "id": 1, "faculty_id": "FAC001", "username": "admin",
        "name": "Dr. Admin", "department": "NSS Cell",
        "email": "admin@mvgrce.edu.in", "phone": "9000000001",
        "password": "admin123", "role": "admin"
    },
]
seed_collection('faculty_members', faculty_data, 'id', lambda d: d['faculty_id'].upper())

print("\n── Seeding volunteers ──")
volunteer_data = [
    {
        "id": 1, "roll_no": "22A91A05B4", "name": "Demo Volunteer",
        "email": "demo@mvgrce.edu.in", "phone": "9000000002",
        "password": "password123", "branch": "CSE", "year": "2nd Year",
        "blood_group": "O+", "address": "MVGR Campus",
        "joined_date": "2024-07-01", "hours": 0, "hours_completed": 0,
        "status": "active"
    },
]
seed_collection('volunteers', volunteer_data, 'id', lambda d: d['roll_no'].upper())

print("\n── Seeding events ──")
event_data = [
    {
        "id": 1, "title": "Blood Donation Camp", "date": "2025-01-15",
        "time": "09:00", "venue": "MVGR Auditorium",
        "description": "Annual blood donation drive organised by NSS.",
        "category": "Health", "hours": 4, "status": "upcoming",
        "organizer": "Dr. Admin", "max_volunteers": 50,
        "registered_volunteers": []
    },
]
seed_collection('events', event_data, 'id', lambda d: str(d['id']))

print("\n── Seeding news_items ──")
news_data = [
    {
        "id": 1, "title": "Welcome to NSS Portal",
        "date": datetime.now().strftime('%Y-%m-%d'),
        "content": "The NSS MVGR portal is now live on Firebase Firestore.",
        "category": "Announcement", "published_by": "Admin",
        "department": "NSS Cell"
    },
]
seed_collection('news_items', news_data, 'id', lambda d: str(d['id']))

print("\n✅ Seeding complete.")
```

---

## Migration Notes

1. **No SQL schema needed** — Firestore is schema-less; documents are created on first write.
2. **Numeric IDs** — Managed by the `_counters` collection. Each collection gets a counter document that tracks `next_id`.
3. **Arrays** — `registered_volunteers` (events) and `present` (attendance_records) are stored as native Firestore arrays (Python lists).
4. **Case-insensitive roll_no search** — Roll numbers are normalised to **uppercase** before storing and querying.
5. **Ordering** — `news_items`, `audit_logs`, and `contacts` are sorted descending by `id` in Python after fetching, avoiding the need for Firestore composite indexes.
