import os
from datetime import datetime
from dotenv import load_dotenv

# Load local environment variables if .env exists
load_dotenv()

firebase_app = None
db = None

def _init_firebase():
    global firebase_app, db
    if firebase_app is not None:
        return True

    service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON', '').strip()
    service_account_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT_PATH', '').strip()

    if not service_account_json and not service_account_path:
        print("ℹ️ Firebase credentials not found in environment. Using in-memory fallback store.")
        return False

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if service_account_json:
            import json
            cred_dict = json.loads(service_account_json)
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate(service_account_path)

        firebase_app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Connected to Firebase Firestore backend successfully.")
        return True
    except Exception as e:
        print(f"⚠️ Failed to initialize Firebase client: {e}")
        return False

_init_firebase()

def is_connected():
    return db is not None

def _get_next_id_simple(collection_name):
    """Simpler (non-transactional) next ID - good enough for low-concurrency portal."""
    counter_ref = db.collection('_counters').document(collection_name)
    snapshot = counter_ref.get()
    if snapshot.exists:
        new_id = snapshot.get('next_id') or 1
    else:
        # Initialize by scanning existing documents
        existing = list(db.collection(collection_name).stream())
        max_id = 0
        for doc in existing:
            data = doc.to_dict()
            if data and isinstance(data.get('id'), int) and data.get('id', 0) > max_id:
                max_id = data['id']
        new_id = max_id + 1
    counter_ref.set({'next_id': new_id + 1})
    return new_id

# ─── VOLUNTEERS ─────────────────────────────────────────────────────────────

def fetch_volunteers(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        docs = db.collection('volunteers').order_by('id').stream()
        result = []
        for doc in docs:
            data = doc.to_dict()
            if data:
                data['hours_completed'] = data.get('hours', data.get('hours_completed', 0))
                data['hours'] = data.get('hours_completed', 0)
                result.append(data)
        return result
    except Exception as e:
        print(f"Firebase fetch_volunteers error: {e}")
        return fallback_list

def get_volunteer_by_roll_no(roll_no):
    if not is_connected() or not roll_no:
        return None
    try:
        clean_roll = roll_no.strip().upper()
        docs = db.collection('volunteers').where('roll_no', '==', clean_roll).limit(1).stream()
        for doc in docs:
            v = doc.to_dict()
            if v:
                v['hours_completed'] = v.get('hours', v.get('hours_completed', 0))
                v['hours'] = v.get('hours_completed', 0)
                return v
    except Exception as e:
        print(f"Firebase get_volunteer_by_roll_no error: {e}")
    return None

def get_volunteer_by_email(email):
    if not is_connected() or not email:
        return None
    try:
        clean_email = email.strip().lower()
        docs = db.collection('volunteers').where('email', '==', clean_email).limit(1).stream()
        for doc in docs:
            v = doc.to_dict()
            if v:
                v['hours_completed'] = v.get('hours', v.get('hours_completed', 0))
                v['hours'] = v.get('hours_completed', 0)
                return v
    except Exception as e:
        print(f"Firebase get_volunteer_by_email error: {e}")
    return None

def insert_volunteer(volunteer_dict):
    hours = volunteer_dict.get('hours_completed', volunteer_dict.get('hours', 0))
    volunteer_dict['hours_completed'] = hours
    volunteer_dict['hours'] = hours
    if is_connected():
        try:
            roll_no = volunteer_dict['roll_no'].strip().upper()
            new_id = _get_next_id_simple('volunteers')
            payload = {
                'id': new_id,
                'roll_no': roll_no,
                'name': volunteer_dict['name'].strip(),
                'email': volunteer_dict['email'].strip(),
                'phone': volunteer_dict.get('phone', '').strip(),
                'password': volunteer_dict.get('password', 'password123'),
                'branch': volunteer_dict.get('branch', 'CSE'),
                'year': volunteer_dict.get('year', '1st Year'),
                'blood_group': volunteer_dict.get('blood_group', 'O+'),
                'address': volunteer_dict.get('address', 'MVGR Campus'),
                'joined_date': volunteer_dict.get('joined_date', datetime.now().strftime('%Y-%m-%d')),
                'hours': hours,
                'hours_completed': hours,
                'status': volunteer_dict.get('status', 'active')
            }
            db.collection('volunteers').document(roll_no).set(payload)
            volunteer_dict.update(payload)
            return payload
        except Exception as e:
            print(f"Firebase insert_volunteer error: {e}")
    return volunteer_dict

def update_volunteer_record(roll_no, updates):
    if is_connected():
        try:
            if 'hours_completed' in updates and 'hours' not in updates:
                updates['hours'] = updates['hours_completed']
            clean_roll = roll_no.strip().upper()
            db.collection('volunteers').document(clean_roll).update(updates)
        except Exception as e:
            print(f"Firebase update_volunteer error: {e}")

# ─── FACULTY ────────────────────────────────────────────────────────────────

def fetch_faculty(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        docs = db.collection('faculty_members').order_by('id').stream()
        result = [doc.to_dict() for doc in docs if doc.to_dict()]
        return result
    except Exception as e:
        print(f"Firebase fetch_faculty error: {e}")
        return fallback_list

def get_faculty_by_email(email):
    if not is_connected() or not email:
        return None
    try:
        clean_email = email.strip().lower()
        docs = db.collection('faculty_members').where('email', '==', clean_email).limit(1).stream()
        for doc in docs:
            f = doc.to_dict()
            if f:
                return f
    except Exception as e:
        print(f"Firebase get_faculty_by_email error: {e}")
    return None

def insert_faculty(faculty_dict):
    if is_connected():
        try:
            faculty_id = faculty_dict.get('faculty_id', '').strip().upper()
            if not faculty_id:
                return faculty_dict
            if 'id' not in faculty_dict:
                faculty_dict['id'] = _get_next_id_simple('faculty_members')
            db.collection('faculty_members').document(faculty_id).set(faculty_dict)
            return faculty_dict
        except Exception as e:
            print(f"Firebase insert_faculty error: {e}")
    return faculty_dict

def update_faculty_record(faculty_id, updates):
    if is_connected():
        try:
            clean_id = faculty_id.strip().upper()
            db.collection('faculty_members').document(clean_id).update(updates)
        except Exception as e:
            print(f"Firebase update_faculty error: {e}")

# ─── EVENTS ─────────────────────────────────────────────────────────────────

def fetch_events(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        docs = db.collection('events').order_by('id').stream()
        result = [doc.to_dict() for doc in docs if doc.to_dict()]
        return result if result else fallback_list
    except Exception as e:
        print(f"Firebase fetch_events error: {e}")
        return fallback_list

def insert_event(event_dict):
    if is_connected():
        try:
            event_id = event_dict.get('id')
            if not event_id:
                event_id = _get_next_id_simple('events')
                event_dict['id'] = event_id
            # Ensure registered_volunteers is a list
            if 'registered_volunteers' not in event_dict:
                event_dict['registered_volunteers'] = []
            db.collection('events').document(str(event_id)).set(event_dict)
            return event_dict
        except Exception as e:
            print(f"Firebase insert_event error: {e}")
    return event_dict

def update_event_record(event_id, updates):
    if is_connected():
        try:
            db.collection('events').document(str(event_id)).update(updates)
        except Exception as e:
            print(f"Firebase update_event error: {e}")

def delete_event_record(event_id):
    if is_connected():
        try:
            db.collection('events').document(str(event_id)).delete()
        except Exception as e:
            print(f"Firebase delete_event error: {e}")

# ─── ATTENDANCE ─────────────────────────────────────────────────────────────

def fetch_attendance(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        docs = db.collection('attendance_records').order_by('id').stream()
        result = [doc.to_dict() for doc in docs if doc.to_dict()]
        return result if result else fallback_list
    except Exception as e:
        print(f"Firebase fetch_attendance error: {e}")
        return fallback_list

def save_attendance(record_dict):
    if is_connected():
        try:
            event_id = record_dict.get('event_id')
            # Check if record for this event already exists (upsert by event_id)
            existing_docs = db.collection('attendance_records').where('event_id', '==', event_id).limit(1).stream()
            existing_doc = None
            for doc in existing_docs:
                existing_doc = doc
                break

            if existing_doc:
                db.collection('attendance_records').document(existing_doc.id).update(record_dict)
            else:
                rec_id = record_dict.get('id') or _get_next_id_simple('attendance_records')
                record_dict['id'] = rec_id
                db.collection('attendance_records').document(str(rec_id)).set(record_dict)
        except Exception as e:
            print(f"Firebase save_attendance error: {e}")

# ─── NEWS ───────────────────────────────────────────────────────────────────

def fetch_news(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        docs = db.collection('news_items').stream()
        result = [doc.to_dict() for doc in docs if doc.to_dict()]
        # Sort descending by id in Python to avoid Firestore composite index requirement
        result.sort(key=lambda x: x.get('id', 0), reverse=True)
        return result if result else fallback_list
    except Exception as e:
        print(f"Firebase fetch_news error: {e}")
        return fallback_list

def insert_news(news_dict):
    if is_connected():
        try:
            news_id = news_dict.get('id') or _get_next_id_simple('news_items')
            news_dict['id'] = news_id
            db.collection('news_items').document(str(news_id)).set(news_dict)
            return news_dict
        except Exception as e:
            print(f"Firebase insert_news error: {e}")
    return news_dict

def delete_news_record(news_id):
    if is_connected():
        try:
            db.collection('news_items').document(str(news_id)).delete()
        except Exception as e:
            print(f"Firebase delete_news error: {e}")

# ─── AUDIT LOGS ─────────────────────────────────────────────────────────────

def fetch_audit_logs(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        docs = db.collection('audit_logs').stream()
        result = [doc.to_dict() for doc in docs if doc.to_dict()]
        # Sort descending by id in Python to avoid Firestore composite index requirement
        result.sort(key=lambda x: x.get('id', 0), reverse=True)
        return result
    except Exception as e:
        print(f"Firebase fetch_audit_logs error: {e}")
        return fallback_list

def insert_audit_log(log_dict):
    if is_connected():
        try:
            log_id = log_dict.get('id') or _get_next_id_simple('audit_logs')
            log_dict['id'] = log_id
            db.collection('audit_logs').document(str(log_id)).set(log_dict)
        except Exception as e:
            print(f"Firebase insert_audit_log error: {e}")

# ─── CONTACTS / INQUIRIES ───────────────────────────────────────────────────

def fetch_contact_messages(fallback_list=None):
    if fallback_list is None:
        fallback_list = []
    if not is_connected():
        return fallback_list
    try:
        docs = db.collection('contacts').stream()
        result = [doc.to_dict() for doc in docs if doc.to_dict()]
        # Sort descending by id in Python
        result.sort(key=lambda x: x.get('id', 0), reverse=True)
        return result if result else fallback_list
    except Exception as e:
        print(f"Firebase fetch_contact_messages error: {e}")
        return fallback_list

def insert_contact_message(msg_dict):
    if is_connected():
        try:
            payload = {
                'name': msg_dict.get('name', '').strip(),
                'email': msg_dict.get('email', '').strip(),
                'subject': msg_dict.get('subject', '').strip(),
                'message': msg_dict.get('message', '').strip(),
                'date': msg_dict.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))
            }
            msg_id = msg_dict.get('id') or _get_next_id_simple('contacts')
            payload['id'] = msg_id
            db.collection('contacts').document(str(msg_id)).set(payload)
            msg_dict['id'] = msg_id
            return payload
        except Exception as e:
            print(f"Firebase insert_contact_message error: {e}")
    return msg_dict
