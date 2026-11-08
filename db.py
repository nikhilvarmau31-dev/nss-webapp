import os
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
        return res.data if res.data else fallback_list
    except Exception as e:
        print(f"Supabase fetch_volunteers error: {e}")
        return fallback_list

def insert_volunteer(volunteer_dict):
    if is_connected():
        try:
            res = supabase_client.table('volunteers').insert(volunteer_dict).execute()
            if res.data:
                return res.data[0]
        except Exception as e:
            print(f"Supabase insert_volunteer error: {e}")
    return volunteer_dict

def update_volunteer_record(roll_no, updates):
    if is_connected():
        try:
            supabase_client.table('volunteers').update(updates).eq('roll_no', roll_no).execute()
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
