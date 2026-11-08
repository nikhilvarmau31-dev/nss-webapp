import os
from datetime import datetime
from dotenv import load_dotenv

# Load local environment variables if .env exists
load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL', '').strip()
SUPABASE_KEY = (os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or 
                os.environ.get('SUPABASE_ANON_KEY') or 
                os.environ.get('SUPABASE_KEY', '')).strip()

supabase_client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(" Connected to Supabase backend successfully.")
    except Exception as e:
        print(f"⚠️ Failed to initialize Supabase client: {e}")
else:
    print("ℹ️ Supabase credentials not found in environment. Using in-memory fallback store.")

def is_connected():
    return supabase_client is not None

# ─── VOLUNTEERS ─────────────────────────────────────────────────────────────

def fetch_volunteers(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        res = supabase_client.table('volunteers').select('*').order('id').execute()
        if res.data:
            # Map Supabase 'hours' column to 'hours_completed' for app compatibility
            for v in res.data:
                v['hours_completed'] = v.get('hours', v.get('hours_completed', 0))
                v['hours'] = v.get('hours_completed', 0)
            return res.data
        return fallback_list
    except Exception as e:
        print(f"Supabase fetch_volunteers error: {e}")
        return fallback_list

def get_volunteer_by_roll_no(roll_no):
    if not is_connected() or not roll_no:
        return None
    try:
        clean_roll = roll_no.strip().upper()
        res = supabase_client.table('volunteers').select('*').ilike('roll_no', clean_roll).execute()
        if res.data and len(res.data) > 0:
            v = res.data[0]
            v['hours_completed'] = v.get('hours', v.get('hours_completed', 0))
            v['hours'] = v.get('hours_completed', 0)
            return v
    except Exception as e:
        print(f"Supabase get_volunteer_by_roll_no error: {e}")
    return None

def insert_volunteer(volunteer_dict):
    # Ensure both hours and hours_completed exist
    hours = volunteer_dict.get('hours_completed', volunteer_dict.get('hours', 0))
    volunteer_dict['hours_completed'] = hours
    volunteer_dict['hours'] = hours
    if is_connected():
        try:
            # Clean payload specifically mapped to Supabase 'volunteers' columns:
            payload = {
                'roll_no': volunteer_dict['roll_no'].strip().upper(),
                'name': volunteer_dict['name'].strip(),
                'email': volunteer_dict['email'].strip(),
                'phone': volunteer_dict.get('phone', '').strip(),
                'password': volunteer_dict.get('password', 'password123'),
                'branch': volunteer_dict.get('branch', 'CSE'),
                'year': volunteer_dict.get('year', '1st Year'),
                'blood_group': volunteer_dict.get('blood_group', 'O+'),
                'address': volunteer_dict.get('address', 'MVGR Campus'),
                'joined_date': volunteer_dict.get('joined_date', datetime.now().strftime('%Y-%m-%d') if 'datetime' in globals() else '2026-11-08'),
                'hours': hours,
                'status': volunteer_dict.get('status', 'active')
            }
            res = supabase_client.table('volunteers').insert(payload).execute()
            if res.data and len(res.data) > 0:
                inserted = res.data[0]
                inserted['hours_completed'] = inserted.get('hours', hours)
                volunteer_dict.update(inserted)
                return inserted
        except Exception as e:
            print(f"Supabase insert_volunteer error: {e}")
    return volunteer_dict

def update_volunteer_record(roll_no, updates):
    if is_connected():
        try:
            # Remap hours_completed to hours if present
            if 'hours_completed' in updates and 'hours' not in updates:
                updates['hours'] = updates['hours_completed']
            clean_updates = {k: v for k, v in updates.items() if k != 'hours_completed'}
            supabase_client.table('volunteers').update(clean_updates).eq('roll_no', roll_no).execute()
        except Exception as e:
            print(f"Supabase update_volunteer error: {e}")

# ─── FACULTY ────────────────────────────────────────────────────────────────

def fetch_faculty(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        res = supabase_client.table('faculty_members').select('*').order('id').execute()
        return res.data if res.data else fallback_list
    except Exception as e:
        print(f"Supabase fetch_faculty error: {e}")
        return fallback_list

def insert_faculty(faculty_dict):
    if is_connected():
        try:
            res = supabase_client.table('faculty_members').insert(faculty_dict).execute()
            if res.data:
                return res.data[0]
        except Exception as e:
            print(f"Supabase insert_faculty error: {e}")
    return faculty_dict

def update_faculty_record(faculty_id, updates):
    if is_connected():
        try:
            supabase_client.table('faculty_members').update(updates).eq('faculty_id', faculty_id).execute()
        except Exception as e:
            print(f"Supabase update_faculty error: {e}")

# ─── EVENTS ─────────────────────────────────────────────────────────────────

def fetch_events(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        res = supabase_client.table('events').select('*').order('id').execute()
        return res.data if res.data else fallback_list
    except Exception as e:
        print(f"Supabase fetch_events error: {e}")
        return fallback_list

def insert_event(event_dict):
    if is_connected():
        try:
            res = supabase_client.table('events').insert(event_dict).execute()
            if res.data:
                return res.data[0]
        except Exception as e:
            print(f"Supabase insert_event error: {e}")
    return event_dict

def update_event_record(event_id, updates):
    if is_connected():
        try:
            supabase_client.table('events').update(updates).eq('id', event_id).execute()
        except Exception as e:
            print(f"Supabase update_event error: {e}")

def delete_event_record(event_id):
    if is_connected():
        try:
            supabase_client.table('events').delete().eq('id', event_id).execute()
        except Exception as e:
            print(f"Supabase delete_event error: {e}")

# ─── ATTENDANCE ─────────────────────────────────────────────────────────────

def fetch_attendance(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        res = supabase_client.table('attendance_records').select('*').order('id').execute()
        return res.data if res.data else fallback_list
    except Exception as e:
        print(f"Supabase fetch_attendance error: {e}")
        return fallback_list

def save_attendance(record_dict):
    if is_connected():
        try:
            # Check if record for this event exists
            existing = supabase_client.table('attendance_records').select('id').eq('event_id', record_dict['event_id']).execute()
            if existing.data:
                supabase_client.table('attendance_records').update(record_dict).eq('id', existing.data[0]['id']).execute()
            else:
                supabase_client.table('attendance_records').insert(record_dict).execute()
        except Exception as e:
            print(f"Supabase save_attendance error: {e}")

# ─── NEWS ───────────────────────────────────────────────────────────────────

def fetch_news(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        res = supabase_client.table('news_items').select('*').order('id', desc=True).execute()
        return res.data if res.data else fallback_list
    except Exception as e:
        print(f"Supabase fetch_news error: {e}")
        return fallback_list

def insert_news(news_dict):
    if is_connected():
        try:
            res = supabase_client.table('news_items').insert(news_dict).execute()
            if res.data:
                return res.data[0]
        except Exception as e:
            print(f"Supabase insert_news error: {e}")
    return news_dict

def delete_news_record(news_id):
    if is_connected():
        try:
            supabase_client.table('news_items').delete().eq('id', news_id).execute()
        except Exception as e:
            print(f"Supabase delete_news error: {e}")

# ─── AUDIT LOGS ─────────────────────────────────────────────────────────────

def fetch_audit_logs(fallback_list):
    if not is_connected():
        return fallback_list
    try:
        res = supabase_client.table('audit_logs').select('*').order('id', desc=True).execute()
        return res.data if res.data else fallback_list
    except Exception as e:
        print(f"Supabase fetch_audit_logs error: {e}")
        return fallback_list

def insert_audit_log(log_dict):
    if is_connected():
        try:
            supabase_client.table('audit_logs').insert(log_dict).execute()
        except Exception as e:
            print(f"Supabase insert_audit_log error: {e}")
