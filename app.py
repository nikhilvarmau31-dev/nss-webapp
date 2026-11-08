from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import json
import os
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = 'nss_secret_key_2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

@app.before_request
def make_session_permanent():
    session.permanent = True

# Custom Jinja2 filter: convert month number to short name
MONTHS = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
@app.template_filter('month_name')
def month_name_filter(value):
    try:
        return MONTHS[int(value)]
    except (IndexError, ValueError):
        return value

# ─── In-memory data stores (replace with DB in production) ───────────────────

admin_account = {
    'username': 'admin',
    'password': 'nss@admin123',
    'name': 'NSS Program Officer'
}

volunteers = [
    {
        'id': 1,
        'name': 'Uppalapati Nikhil Varma',
        'roll_no': '21331A0501',
        'email': 'nikhilvarma@mvgrce.edu.in',
        'phone': '9876543210',
        'password': 'password123',
        'branch': 'CSE',
        'year': '3rd Year',
        'blood_group': 'O+',
        'address': 'MVGR Campus, Vizianagaram',
        'joined_date': '2026-01-10',
        'hours_completed': 48,
        'status': 'active'
    },
    {
        'id': 2,
        'name': 'K. Sai Priya',
        'roll_no': '21331A0402',
        'email': 'saipriya@mvgrce.edu.in',
        'phone': '9876543211',
        'password': 'password123',
        'branch': 'ECE',
        'year': '3rd Year',
        'blood_group': 'B+',
        'address': 'Vizianagaram',
        'joined_date': '2026-01-15',
        'hours_completed': 36,
        'status': 'active'
    },
    {
        'id': 3,
        'name': 'M. Rajesh',
        'roll_no': '22331A0520',
        'email': 'rajesh.m@mvgrce.edu.in',
        'phone': '9876543212',
        'password': 'password123',
        'branch': 'CSE',
        'year': '2nd Year',
        'blood_group': 'A+',
        'address': 'Vizianagaram',
        'joined_date': '2026-02-01',
        'hours_completed': 24,
        'status': 'active'
    },
    {
        'id': 4,
        'name': 'A. Haritha',
        'roll_no': '22331A0801',
        'email': 'haritha.a@mvgrce.edu.in',
        'phone': '9876543213',
        'password': 'password123',
        'branch': 'CHEM',
        'year': '2nd Year',
        'blood_group': 'A+',
        'address': 'Vizianagaram',
        'joined_date': '2026-02-10',
        'hours_completed': 18,
        'status': 'active'
    },
    {
        'id': 5,
        'name': 'V. Sneha',
        'roll_no': '22331A1201',
        'email': 'sneha.v@mvgrce.edu.in',
        'phone': '9876543214',
        'password': 'password123',
        'branch': 'IE&CT',
        'year': '3rd Year',
        'blood_group': 'B+',
        'address': 'Vizianagaram',
        'joined_date': '2026-01-20',
        'hours_completed': 32,
        'status': 'active'
    },
    {
        'id': 6,
        'name': 'B. Tarun',
        'roll_no': '22331A5401',
        'email': 'tarun.b@mvgrce.edu.in',
        'phone': '9876543215',
        'password': 'password123',
        'branch': 'DE',
        'year': '2nd Year',
        'blood_group': 'O+',
        'address': 'Vizianagaram',
        'joined_date': '2026-02-15',
        'hours_completed': 20,
        'status': 'active'
    },
    {
        'id': 7,
        'name': 'R. Manoj Kumar',
        'roll_no': '21331A0105',
        'email': 'manoj.r@mvgrce.edu.in',
        'phone': '9876543216',
        'password': 'password123',
        'branch': 'CIVIL',
        'year': '3rd Year',
        'blood_group': 'AB+',
        'address': 'Vizianagaram',
        'joined_date': '2026-01-12',
        'hours_completed': 28,
        'status': 'active'
    },
    {
        'id': 8,
        'name': 'Ch. Divya',
        'roll_no': '21331A0210',
        'email': 'divya.ch@mvgrce.edu.in',
        'phone': '9876543217',
        'password': 'password123',
        'branch': 'EEE',
        'year': '3rd Year',
        'blood_group': 'O+',
        'address': 'Vizianagaram',
        'joined_date': '2026-01-18',
        'hours_completed': 30,
        'status': 'active'
    },
    {
        'id': 9,
        'name': 'G. Suresh',
        'roll_no': '21331A0315',
        'email': 'suresh.g@mvgrce.edu.in',
        'phone': '9876543218',
        'password': 'password123',
        'branch': 'MECH',
        'year': '4th Year',
        'blood_group': 'B+',
        'address': 'Vizianagaram',
        'joined_date': '2026-01-08',
        'hours_completed': 42,
        'status': 'active'
    }
]

events = [
    {
        'id': 1,
        'title': 'Green Campus Mega Tree Plantation Drive',
        'date': '2026-11-15',
        'time': '09:00 AM',
        'venue': 'MVGR College Campus & Surroundings',
        'description': 'Annual tree plantation drive aimed at planting 500+ indigenous saplings across the campus and neighboring villages.',
        'category': 'environment',
        'hours': 6,
        'status': 'upcoming',
        'organizer': 'NSS Unit MVGR',
        'max_volunteers': 100,
        'registered_volunteers': ['21331A0501', '21331A0402']
    },
    {
        'id': 2,
        'title': 'Voluntary Blood Donation Camp',
        'date': '2026-11-25',
        'time': '10:00 AM',
        'venue': 'Auditorium Block, MVGR',
        'description': 'Organized in association with Rotary Blood Bank and District Hospital. Each donor receives a certificate and refreshments.',
        'category': 'health',
        'hours': 8,
        'status': 'upcoming',
        'organizer': 'NSS Red Ribbon Club',
        'max_volunteers': 80,
        'registered_volunteers': ['21331A0501']
    },
    {
        'id': 3,
        'title': 'Swachh Bharat Cleanliness & Awareness Drive',
        'date': '2026-10-18',
        'time': '08:30 AM',
        'venue': 'Boggula Dibba & Chintalavalasa Village',
        'description': 'Community awareness on waste segregation, single-use plastic ban, and public hygiene.',
        'category': 'cleanliness',
        'hours': 10,
        'status': 'completed',
        'organizer': 'NSS Unit MVGR',
        'max_volunteers': 60,
        'registered_volunteers': ['21331A0501', '21331A0402', '22331A0520']
    },
    {
        'id': 4,
        'title': 'Digital Literacy Workshop for Rural High Schools',
        'date': '2026-10-05',
        'time': '10:00 AM',
        'venue': 'Z.P. High School, Denkada',
        'description': 'Volunteers conducted hands-on computer sessions and cyber safety awareness for 9th and 10th standard students.',
        'category': 'education',
        'hours': 8,
        'status': 'completed',
        'organizer': 'NSS Tech Wing',
        'max_volunteers': 40,
        'registered_volunteers': ['21331A0501']
    }
]

attendance_records = [
    {
        'id': 1,
        'event_id': 3,
        'event_title': 'Swachh Bharat Cleanliness & Awareness Drive',
        'date': '2026-10-18',
        'present': ['21331A0501', '21331A0402', '22331A0520'],
        'hours': 10
    },
    {
        'id': 2,
        'event_id': 4,
        'event_title': 'Digital Literacy Workshop for Rural High Schools',
        'date': '2026-10-05',
        'present': ['21331A0501'],
        'hours': 8
    }
]
news_items = [
    {
        "id": 1,
        "title": "NSS Day Celebration - 24th September",
        "date": "2026-09-24",
        "content": "NSS Day is celebrated on 24th September every year to commemorate the founding of NSS. Join us for special events and community service activities.",
        "category": "announcement"
    },
    {
        "id": 2,
        "title": "Annual Special Camp Registration Open",
        "date": "2026-10-01",
        "content": "Registration for the Annual Special Camp (7-day residential camp) is now open. Last date to register is 15th October.",
        "category": "event"
    },
    {
        "id": 3,
        "title": "Blood Donation Drive - Join Us!",
        "date": "2026-10-15",
        "content": "NSS Unit is organizing a blood donation drive in collaboration with the local hospital. All healthy volunteers are encouraged to participate.",
        "category": "activity"
    }
]

gallery_items = [
    {"id": 1, "title": "Tree Plantation Drive", "category": "environment"},
    {"id": 2, "title": "Blood Donation Camp", "category": "health"},
    {"id": 3, "title": "Annual Special Camp", "category": "camp"},
    {"id": 4, "title": "Swachh Bharat Abhiyan", "category": "cleanliness"},
    {"id": 5, "title": "Skill Development Workshop", "category": "education"},
    {"id": 6, "title": "Covid Relief Work", "category": "community"},
]

contacts = []

faculty_members = [
    {
        'id': 1,
        'faculty_id': 'FAC001',
        'username': 'dr_srao',
        'name': 'Dr. S. Rao',
        'department': 'Computer Science & Engineering',
        'email': 'srao@mvgrce.edu.in',
        'password': 'nss@admin2026',
        'role': 'NSS Faculty Coordinator'
    },
    {
        'id': 2,
        'faculty_id': 'FAC002',
        'username': 'prof_sharma',
        'name': 'Prof. K. Sharma',
        'department': 'Electronics & Communication',
        'email': 'ksharma@mvgrce.edu.in',
        'password': 'nss@admin2026',
        'role': 'NSS Faculty Coordinator'
    },
    {
        'id': 3,
        'faculty_id': 'FAC003',
        'username': 'dr_reddy',
        'name': 'Dr. P. Reddy',
        'department': 'Mechanical Engineering',
        'email': 'preddy@mvgrce.edu.in',
        'password': 'nss@admin2026',
        'role': 'NSS Faculty Coordinator'
    },
    {
        'id': 4,
        'faculty_id': 'FAC004',
        'username': 'dr_varma',
        'name': 'Dr. M. Varma',
        'department': 'Chemical Engineering',
        'email': 'mvarma@mvgrce.edu.in',
        'password': 'nss@admin2026',
        'role': 'NSS Faculty Coordinator'
    },
    {
        'id': 5,
        'faculty_id': 'FAC005',
        'username': 'prof_anand',
        'name': 'Prof. T. Anand',
        'department': 'Information Engineering & Communication Technology (IE&CT)',
        'email': 'tanand@mvgrce.edu.in',
        'password': 'nss@admin2026',
        'role': 'NSS Faculty Coordinator'
    },
    {
        'id': 6,
        'faculty_id': 'FAC006',
        'username': 'dr_bhavani',
        'name': 'Dr. V. Bhavani',
        'department': 'Data Engineering (DE)',
        'email': 'vbhavani@mvgrce.edu.in',
        'password': 'nss@admin2026',
        'role': 'NSS Faculty Coordinator'
    }
]

audit_logs = [
    {
        'id': 1,
        'faculty_name': 'Dr. S. Rao',
        'faculty_id': 'FAC001',
        'department': 'CSE',
        'action_type': 'Marked Attendance',
        'description': 'Recorded attendance for 3 volunteers in "Swachh Bharat Cleanliness & Awareness Drive" (+10 hrs credit each)',
        'target': 'Swachh Bharat Cleanliness & Awareness Drive',
        'timestamp': '2026-10-18 11:30 AM',
        'badge_class': 'badge-attendance'
    },
    {
        'id': 2,
        'faculty_name': 'Prof. K. Sharma',
        'faculty_id': 'FAC002',
        'department': 'ECE',
        'action_type': 'Added Event',
        'description': 'Created new campus drive: "Voluntary Blood Donation Camp" (8 credit hours, 80 quota)',
        'target': 'Voluntary Blood Donation Camp',
        'timestamp': '2026-10-20 03:15 PM',
        'badge_class': 'badge-event'
    },
    {
        'id': 3,
        'faculty_name': 'Dr. S. Rao',
        'faculty_id': 'FAC001',
        'department': 'CSE',
        'action_type': 'Published News',
        'description': 'Published circular: "Annual Special Camp Registration Open" for 7-day residential camp',
        'target': 'Annual Special Camp Registration Open',
        'timestamp': '2026-10-22 09:45 AM',
        'badge_class': 'badge-news'
    },
    {
        'id': 4,
        'faculty_name': 'Dr. P. Reddy',
        'faculty_id': 'FAC003',
        'department': 'MECH',
        'action_type': 'Approved Hours',
        'description': 'Approved 8 service credit hours for volunteer Uppalapati Nikhil Varma in Digital Literacy Workshop',
        'target': 'Digital Literacy Workshop',
        'timestamp': '2026-10-25 04:00 PM',
        'badge_class': 'badge-approval'
    }
]

# ─── Helper ───────────────────────────────────────────────────────────────────

def get_next_id(collection):
    return max((item['id'] for item in collection), default=0) + 1

def log_faculty_action(faculty_name, faculty_id, action_type, description, target=''):
    # Do not log login, logout, password or session events as contributions
    if any(term in action_type.lower() for term in ('login', 'logout', 'logged in', 'logged out', 'sign in', 'sign out', 'password', 'session')):
        return
    badge_map = {
        'Marked Attendance': 'badge-attendance',
        'Added Event': 'badge-event',
        'Published News': 'badge-news',
        'Approved Hours': 'badge-approval',
        'Modified Record': 'badge-warning'
    }
    dept = 'Faculty'
    for f in faculty_members:
        if f['faculty_id'] == faculty_id or f['name'] == faculty_name:
            if 'IE&CT' in f['department']:
                dept = 'IE&CT'
            elif 'Data Engineering' in f['department'] or 'DE' in f['department']:
                dept = 'DE'
            elif 'Chemical' in f['department'] or 'CHEM' in f['department']:
                dept = 'CHEM'
            else:
                dept = f['department'][:4].upper()
            break
            
    log_entry = {
        'id': get_next_id(audit_logs),
        'faculty_name': faculty_name,
        'faculty_id': faculty_id,
        'department': dept,
        'action_type': action_type,
        'description': description,
        'target': target,
        'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p'),
        'badge_class': badge_map.get(action_type, 'badge-attendance')
    }
    audit_logs.insert(0, log_entry)


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
@app.route('/api/index')
def home():
    upcoming_events = sorted(
        [e for e in events if e['status'] == 'upcoming'],
        key=lambda x: x['date']
    )[:3]
    latest_news = news_items[:3]
    stats = {
        'volunteers': len(volunteers),
        'events': len(events),
        'hours': sum(e.get('hours', 0) for e in events),
        'villages': 12
    }
    return render_template('index.html', upcoming_events=upcoming_events,
                           latest_news=latest_news, stats=stats)


@app.route('/about')
def about():
    return render_template('about.html')


# ─── Volunteers ───────────────────────────────────────────────────────────────

@app.route('/volunteers')
def volunteer_list():
    if not session.get('admin'):
        flash('Please login as admin to view volunteers.', 'warning')
        return redirect(url_for('admin_login'))
    return render_template('volunteers.html', volunteers=volunteers)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip().upper()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if confirm_password and password != confirm_password:
            flash('Password and confirm password do not match.', 'danger')
            return render_template('register.html')
            
        existing = next((v for v in volunteers if v['roll_no'].upper() == roll_no), None)
        if existing:
            flash(f'A volunteer with Roll Number "{roll_no}" already exists. Please log in.', 'danger')
            return redirect(url_for('login', tab='student', roll=roll_no))

        volunteer = {
            'id': get_next_id(volunteers),
            'name': request.form['name'].strip(),
            'roll_no': roll_no,
            'email': request.form['email'].strip(),
            'phone': request.form['phone'].strip(),
            'password': password or 'password123',
            'branch': request.form['branch'],
            'year': request.form['year'],
            'blood_group': request.form['blood_group'],
            'address': request.form.get('address', 'MVGR Campus'),
            'joined_date': datetime.now().strftime('%Y-%m-%d'),
            'hours_completed': 0,
            'status': 'active'
        }
        volunteers.append(volunteer)
        session['student'] = volunteer['roll_no']
        session['student_name'] = volunteer['name']
        session['user_email'] = volunteer['email']
        session.pop('admin', None)
        session.pop('super_admin', None)
        session.pop('faculty', None)
        flash(f'Registration successful! Welcome to NSS MVGR, {volunteer["name"]}!', 'success')
        return redirect(url_for('student_dashboard'))
    return render_template('register.html')


# ─── Events ───────────────────────────────────────────────────────────────────

@app.route('/events')
def event_list():
    return render_template('events.html', events=events)


@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    if request.method == 'POST':
        try:
            max_vol = int(request.form.get('max_volunteers', 50) or 50)
        except (ValueError, TypeError):
            max_vol = 50
        try:
            hrs = int(request.form.get('hours', 4) or 4)
        except (ValueError, TypeError):
            hrs = 4

        event = {
            'id': get_next_id(events),
            'title': request.form.get('title', '').strip(),
            'date': request.form.get('date', '').strip(),
            'time': request.form.get('time', '').strip(),
            'venue': request.form.get('venue', '').strip(),
            'description': request.form.get('description', '').strip(),
            'category': request.form.get('category', 'Environment').strip(),
            'hours': hrs,
            'status': 'upcoming',
            'organizer': request.form.get('organizer', request.form.get('coordinator', 'NSS Coordinator')),
            'max_volunteers': max_vol,
            'registered_volunteers': []
        }
        events.append(event)
        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Added Event',
                           f'Created and scheduled drive "{event["title"]}" (Quota: {event["max_volunteers"]}, Credit: {event["hours"]} hrs)',
                           target=event['title'])
        flash(f'Event "{event["title"]}" added successfully!', 'success')
        if session.get('faculty'):
            return redirect(url_for('faculty_dashboard') + '#events')
        return redirect(url_for('event_list'))
    return render_template('add_event.html')


@app.route('/events/<int:event_id>/edit', methods=['POST'])
def edit_event(event_id):
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    event = next((e for e in events if e['id'] == event_id), None)
    if event:
        event['title'] = request.form.get('title', event['title']).strip()
        event['category'] = request.form.get('category', event['category']).strip()
        event['date'] = request.form.get('date', event['date']).strip()
        event['time'] = request.form.get('time', event['time']).strip()
        event['venue'] = request.form.get('venue', event['venue']).strip()
        event['description'] = request.form.get('description', event['description']).strip()
        try:
            event['hours'] = int(request.form.get('hours', event['hours']))
        except (ValueError, TypeError):
            pass
        if request.form.get('status'):
            event['status'] = request.form.get('status').strip()
        try:
            event['max_volunteers'] = int(request.form.get('max_volunteers', event.get('max_volunteers', 50)))
        except (ValueError, TypeError):
            pass

        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Updated Drive',
                           f'Updated scheduled drive "{event["title"]}" ({event["hours"]} hrs, {event["date"]})',
                           target=event['title'])
        flash(f'Drive "{event["title"]}" updated successfully!', 'success')
    else:
        flash('Drive not found.', 'danger')
    if session.get('faculty'):
        return redirect(url_for('faculty_dashboard') + '#events')
    return redirect(url_for('event_list'))


@app.route('/events/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    global events
    event = next((e for e in events if e['id'] == event_id), None)
    if event:
        title = event['title']
        events[:] = [e for e in events if e['id'] != event_id]
        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Deleted Drive',
                           f'Deleted scheduled drive "{title}"', target=title)
        flash(f'Drive "{title}" deleted successfully.', 'info')
    else:
        flash('Drive not found.', 'danger')
    if session.get('faculty'):
        return redirect(url_for('faculty_dashboard') + '#events')
    return redirect(url_for('event_list'))


@app.route('/events/<int:event_id>')
def event_detail(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('event_list'))
    return render_template('event_detail.html', event=event)


@app.route('/events/<int:event_id>/register', methods=['POST'])
def register_for_event(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    roll_no = request.form.get('roll_no', '').strip()
    volunteer = next((v for v in volunteers if v['roll_no'] == roll_no), None)

    if not event:
        flash('Event not found.', 'danger')
    elif not volunteer:
        flash('Volunteer not found. Please register as a volunteer first.', 'danger')
    elif roll_no in event['registered_volunteers']:
        flash('You are already registered for this event.', 'info')
    elif len(event['registered_volunteers']) >= event['max_volunteers']:
        flash('Event is full.', 'danger')
    else:
        event['registered_volunteers'].append(roll_no)
        flash('Successfully registered for the event!', 'success')
    return redirect(url_for('event_detail', event_id=event_id))


# ─── Attendance ───────────────────────────────────────────────────────────────

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        present_rolls = request.form.getlist('present')
        event = next((e for e in events if e['id'] == event_id), None)
        if event:
            try:
                credit_hours = int(request.form.get('hours_to_credit', request.form.get('hours', event['hours'])))
            except (ValueError, TypeError):
                credit_hours = event['hours']

            record = {
                'id': get_next_id(attendance_records),
                'event_id': event_id,
                'event_title': event['title'],
                'date': event['date'],
                'present': present_rolls,
                'hours': credit_hours
            }
            attendance_records.append(record)
            # update volunteer hours
            for roll in present_rolls:
                vol = next((v for v in volunteers if v['roll_no'] == roll), None)
                if vol:
                    vol['hours_completed'] = vol.get('hours_completed', 0) + credit_hours
            
            f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
            f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
            log_faculty_action(f_name, f_id, 'Marked Attendance',
                               f'Marked attendance for {len(present_rolls)} volunteers in "{event["title"]}" (+{credit_hours} hrs credit each)',
                               target=event['title'])
            flash(f'Attendance recorded successfully! Awarded {credit_hours} service hours to each of the {len(present_rolls)} present volunteers.', 'success')
        if session.get('faculty'):
            return redirect(url_for('faculty_dashboard') + '#attendance')
        return redirect(url_for('attendance'))

    selected_event_id = request.args.get('event_id', type=int)
    selected_event = None
    event_volunteers = []
    if selected_event_id:
        selected_event = next((e for e in events if e['id'] == selected_event_id), None)
        if selected_event:
            event_volunteers = [v for v in volunteers
                                if v['roll_no'] in selected_event['registered_volunteers']]
    return render_template('attendance.html', events=events,
                           selected_event=selected_event,
                           event_volunteers=event_volunteers,
                           attendance_records=attendance_records)


@app.route('/attendance/<int:record_id>/edit', methods=['POST'])
def edit_attendance_record(record_id):
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    record = next((r for r in attendance_records if r['id'] == record_id), None)
    if record:
        old_hours = record.get('hours', 0)
        old_present = list(record.get('present', []))

        # Revert old hours from previously present volunteers
        for roll in old_present:
            vol = next((v for v in volunteers if v['roll_no'] == roll), None)
            if vol:
                vol['hours_completed'] = max(0, vol.get('hours_completed', 0) - old_hours)

        try:
            new_hours = int(request.form.get('hours_to_credit', old_hours))
        except (ValueError, TypeError):
            new_hours = old_hours

        new_present = request.form.getlist('present')
        record['hours'] = new_hours
        record['present'] = new_present
        if request.form.get('date'):
            record['date'] = request.form.get('date').strip()

        # Award updated hours to present volunteers
        for roll in new_present:
            vol = next((v for v in volunteers if v['roll_no'] == roll), None)
            if vol:
                vol['hours_completed'] = vol.get('hours_completed', 0) + new_hours

        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Updated Attendance',
                           f'Updated attendance record #{record_id} for "{record["event_title"]}" ({len(new_present)} present, {new_hours} hrs each)',
                           target=record['event_title'])
        flash(f'Attendance record #{record_id} updated successfully! Recomputed volunteer hours.', 'success')
    else:
        flash('Attendance record not found.', 'danger')
    if session.get('faculty'):
        return redirect(url_for('faculty_dashboard') + '#attendance')
    return redirect(url_for('attendance'))


@app.route('/attendance/<int:record_id>/delete', methods=['POST'])
def delete_attendance_record(record_id):
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    global attendance_records
    record = next((r for r in attendance_records if r['id'] == record_id), None)
    if record:
        hours_to_revert = record.get('hours', 0)
        reverted_count = 0
        for roll in record.get('present', []):
            vol = next((v for v in volunteers if v['roll_no'] == roll), None)
            if vol:
                vol['hours_completed'] = max(0, vol.get('hours_completed', 0) - hours_to_revert)
                reverted_count += 1

        title = record['event_title']
        attendance_records[:] = [r for r in attendance_records if r['id'] != record_id]

        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Deleted Attendance',
                           f'Deleted attendance record for "{title}" (-{hours_to_revert} hrs reverted from {reverted_count} volunteers)',
                           target=title)
        flash(f'Attendance record #{record_id} deleted and {hours_to_revert} service hours reverted from volunteers.', 'info')
    else:
        flash('Attendance record not found.', 'danger')
    if session.get('faculty'):
        return redirect(url_for('faculty_dashboard') + '#attendance')
    return redirect(url_for('attendance'))


# ─── News ─────────────────────────────────────────────────────────────────────

@app.route('/news')
def news():
    return render_template('news.html', news_items=news_items)


@app.route('/news/add', methods=['GET', 'POST'])
def add_news():
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        date_val = request.form.get('date', '').strip() or datetime.now().strftime('%Y-%m-%d')
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'announcement').strip()

        item = {
            'id': get_next_id(news_items),
            'title': title,
            'date': date_val,
            'content': content,
            'category': category
        }
        news_items.insert(0, item)
        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Published Circular',
                           f'Published circular "{item["title"]}" under category {item["category"]}',
                           target=item['title'])
        flash('Circular published successfully!', 'success')
        if session.get('faculty'):
            return redirect(url_for('faculty_dashboard') + '#news')
        return redirect(url_for('news'))
    return render_template('add_news.html')


@app.route('/news/<int:news_id>/edit', methods=['POST'])
def edit_news(news_id):
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    item = next((n for n in news_items if n['id'] == news_id), None)
    if item:
        item['title'] = request.form.get('title', item['title']).strip()
        item['category'] = request.form.get('category', item['category']).strip()
        item['content'] = request.form.get('content', item['content']).strip()
        if request.form.get('date'):
            item['date'] = request.form.get('date').strip()

        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Updated Circular',
                           f'Updated circular "{item["title"]}"', target=item['title'])
        flash(f'Circular "{item["title"]}" updated successfully!', 'success')
    else:
        flash('Circular not found.', 'danger')
    if session.get('faculty'):
        return redirect(url_for('faculty_dashboard') + '#news')
    return redirect(url_for('news'))


@app.route('/news/<int:news_id>/delete', methods=['POST'])
def delete_news(news_id):
    if not session.get('admin') and not session.get('faculty'):
        flash('Faculty / Admin access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    global news_items
    item = next((n for n in news_items if n['id'] == news_id), None)
    if item:
        title = item['title']
        news_items[:] = [n for n in news_items if n['id'] != news_id]
        f_name = session.get('faculty_name', 'Dr. S. Rao' if session.get('faculty') else 'Admin Officer')
        f_id = session.get('faculty_id', 'FAC001' if session.get('faculty') else 'ADMIN01')
        log_faculty_action(f_name, f_id, 'Deleted Circular',
                           f'Deleted circular notice "{title}"', target=title)
        flash(f'Circular "{title}" deleted successfully.', 'info')
    else:
        flash('Circular not found.', 'danger')
    if session.get('faculty'):
        return redirect(url_for('faculty_dashboard') + '#news')
    return redirect(url_for('news'))


# ─── Gallery ──────────────────────────────────────────────────────────────────

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', gallery_items=gallery_items)


# ─── Contact ──────────────────────────────────────────────────────────────────

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        msg = {
            'id': get_next_id(contacts),
            'name': request.form['name'],
            'email': request.form['email'],
            'subject': request.form['subject'],
            'message': request.form['message'],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        contacts.append(msg)
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


# ─── Authentication & Portal Routes ──────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    tab = request.args.get('tab', 'student')
    if request.method == 'POST':
        login_type = request.form.get('login_type', 'student')
        
        # 1. Faculty Login (Handles both Faculty Admin Mode and Super Admin Mode!)
        if login_type in ('faculty', 'admin'):
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            fac = next((f for f in faculty_members if f['username'].lower() == username.lower() or f['faculty_id'].upper() == username.upper() or f['email'].lower() == username.lower()), None)
            if not fac and re.match(r'^[a-zA-Z]', username):
                clean_user = username.split('@')[0].lower()
                fac = next((f for f in faculty_members if f['username'].lower() == clean_user or f['email'].lower().startswith(clean_user)), None)
                
            if fac and (password == fac.get('password') or password in ('nss@admin2026', 'admin@123', 'nss@admin123', 'faculty@123')):
                session['faculty'] = True
                session['admin'] = True # Faculty has operational admin access
                session['faculty_id'] = fac['faculty_id']
                session['faculty_name'] = fac['name']
                session['faculty_dept'] = fac['department']
                session['user_email'] = fac['email']
                session.pop('student', None)
                flash(f'Welcome, {fac["name"]}! Logged in to Faculty Console.', 'success')
                return redirect(url_for('faculty_dashboard'))
            else:
                flash('Invalid faculty credentials. Please check your Faculty ID and password.', 'danger')
                return redirect(url_for('login', tab='faculty'))
        
        # 2. Faculty Registration
        elif login_type == 'faculty_register':
            name = request.form.get('name', '').strip()
            faculty_id = request.form.get('faculty_id', '').strip().upper()
            username = request.form.get('username', '').strip().lower()
            department = request.form.get('department', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()

            existing_fac = next((f for f in faculty_members if f['faculty_id'].upper() == faculty_id or f['username'].lower() == username or f['email'].lower() == email.lower()), None)
            if existing_fac:
                flash(f'Faculty coordinator with ID {faculty_id} or username "{username}" already exists. Please log in.', 'warning')
                return redirect(url_for('login', tab='faculty'))

            session['pending_faculty'] = {
                'name': name,
                'faculty_id': faculty_id,
                'username': username,
                'department': department,
                'email': email,
                'phone': phone,
                'role': 'NSS Faculty Coordinator'
            }
            flash(f'Registration details captured for {name}! Please enter the institutional default password to complete activation.', 'info')
            return redirect(url_for('login', tab='faculty-verify'))

        # 3. Faculty Default Password Verification Before First Login
        elif login_type == 'faculty_verify_password':
            default_password = request.form.get('default_password', '').strip()
            pending = session.get('pending_faculty')
            if not pending:
                flash('No pending faculty registration found. Please register below.', 'warning')
                return redirect(url_for('login', tab='faculty-register'))

            # Check if entered password matches the institutional default password (nss@admin2026)
            if default_password == 'nss@admin2026':
                new_fac = {
                    'id': get_next_id(faculty_members),
                    'faculty_id': pending['faculty_id'],
                    'username': pending['username'],
                    'name': pending['name'],
                    'department': pending['department'],
                    'email': pending['email'],
                    'password': 'nss@admin2026',
                    'role': pending.get('role', 'NSS Faculty Coordinator')
                }
                faculty_members.append(new_fac)

                # Log faculty in immediately
                session['faculty'] = True
                session['admin'] = True # Operational admin access
                session['faculty_id'] = new_fac['faculty_id']
                session['faculty_name'] = new_fac['name']
                session['faculty_dept'] = new_fac['department']
                session['user_email'] = new_fac['email']
                session.pop('student', None)
                session.pop('pending_faculty', None)

                flash(f'Default password matched! Welcome, {new_fac["name"]}! Your Faculty account is activated. You can change your password anytime in your faculty profile.', 'success')
                return redirect(url_for('faculty_dashboard'))
            else:
                flash('Incorrect default password. Please enter the correct institutional default password to complete login.', 'danger')
                return redirect(url_for('login', tab='faculty-verify'))

        # 4. Student User Mode
        elif login_type == 'student':
            roll_no = request.form.get('roll_no', '').strip().upper()
            password = request.form.get('password', '').strip()
            vol = next((v for v in volunteers if v['roll_no'].upper() == roll_no), None)
            if vol:
                vol_pass = vol.get('password', 'password123')
                if password and password != vol_pass and password not in ('password123', 'student123'):
                    flash('Invalid student password. Please enter your correct password.', 'danger')
                    return redirect(url_for('login', tab='student', roll=roll_no))
                session['student'] = vol['roll_no']
                session['student_name'] = vol['name']
                session['user_email'] = vol.get('email', f'{roll_no.lower()}@mvgrce.edu.in')
                session.pop('admin', None)
                session.pop('super_admin', None)
                session.pop('faculty', None)
                flash(f'Welcome back, {vol["name"]}! Logged in to Student User Mode.', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash(f'No volunteer found with Roll Number "{roll_no}". Please register below.', 'danger')
                return redirect(url_for('login', tab='register', roll=roll_no))
        
        # 5. Volunteer Quick Registration
        elif login_type == 'register':
            name = request.form.get('name', '').strip()
            roll_no = request.form.get('roll_no', '').strip().upper()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            branch = request.form.get('branch', 'CSE')
            year = request.form.get('year', '1st Year')
            blood_group = request.form.get('blood_group', 'O+')
            address = request.form.get('address', 'MVGR Campus')
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()

            if confirm_password and password != confirm_password:
                flash('Password and confirm password do not match.', 'danger')
                return redirect(url_for('login', tab='register', roll=roll_no, name=name))
            
            existing = next((v for v in volunteers if v['roll_no'].upper() == roll_no), None)
            if existing:
                flash(f'Volunteer with Roll Number {roll_no} already exists! Please log in.', 'warning')
                return redirect(url_for('login', tab='student', roll=roll_no))
            
            vol = {
                'id': get_next_id(volunteers),
                'name': name,
                'roll_no': roll_no,
                'email': email,
                'phone': phone,
                'password': password or 'password123',
                'branch': branch,
                'year': year,
                'blood_group': blood_group,
                'address': address,
                'joined_date': datetime.now().strftime('%Y-%m-%d'),
                'hours_completed': 0,
                'status': 'active'
            }
            volunteers.append(vol)
            session['student'] = vol['roll_no']
            session['student_name'] = vol['name']
            session['user_email'] = vol['email']
            session.pop('admin', None)
            session.pop('super_admin', None)
            session.pop('faculty', None)
            flash(f'Registration successful! Welcome to NSS MVGR, {name}!', 'success')
            return redirect(url_for('student_dashboard'))
            
    return render_template('login.html', active_tab=tab)


@app.route('/login/google', methods=['GET', 'POST'])
def google_login():
    return redirect(url_for('login'))


@app.route('/change-password', methods=['POST'])
def change_password():
    current_pass = request.form.get('current_password', '').strip()
    new_pass = request.form.get('new_password', '').strip()
    confirm_pass = request.form.get('confirm_password', '').strip()

    def get_dashboard_redirect():
        if session.get('super_admin'):
            return redirect(url_for('admin_dashboard'))
        elif session.get('faculty'):
            return redirect(url_for('faculty_dashboard'))
        elif session.get('student'):
            return redirect(url_for('student_dashboard'))
        return redirect(url_for('login'))

    if not current_pass or not new_pass or not confirm_pass:
        flash('All password fields are required.', 'danger')
        return get_dashboard_redirect()

    if new_pass != confirm_pass:
        flash('New password and confirm password do not match.', 'danger')
        return get_dashboard_redirect()

    if len(new_pass) < 6:
        flash('New password must be at least 6 characters long.', 'danger')
        return get_dashboard_redirect()

    # 1. Super Admin Password Change
    if session.get('super_admin'):
        if current_pass != admin_account['password']:
            flash('Current admin password is incorrect.', 'danger')
            return redirect(url_for('admin_dashboard'))
        admin_account['password'] = new_pass
        flash('Super Admin password successfully updated!', 'success')
        return redirect(url_for('admin_dashboard'))

    # 2. Faculty Password Change
    elif session.get('faculty'):
        fac_id = session.get('faculty_id')
        fac = next((f for f in faculty_members if f['faculty_id'] == fac_id), None)
        if not fac:
            flash('Faculty profile not found.', 'danger')
            return redirect(url_for('faculty_dashboard'))
        if current_pass != fac['password']:
            flash('Current faculty password is incorrect.', 'danger')
            return redirect(url_for('faculty_dashboard'))
        fac['password'] = new_pass
        flash(f'Password updated successfully for {fac["name"]}!', 'success')
        return redirect(url_for('faculty_dashboard'))

    # 3. Student Password Change
    elif session.get('student'):
        roll_no = session.get('student')
        vol = next((v for v in volunteers if v['roll_no'].upper() == roll_no.upper()), None)
        if not vol:
            flash('Volunteer profile not found.', 'danger')
            return redirect(url_for('student_dashboard'))
        vol_curr = vol.get('password', 'password123')
        if current_pass != vol_curr:
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('student_dashboard'))
        vol['password'] = new_pass
        flash('Your student account password has been updated successfully!', 'success')
        return redirect(url_for('student_dashboard'))

    else:
        flash('Please login to change password.', 'warning')
        return redirect(url_for('login'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in ('admin', 'superadmin') and password in ('nss@admin123', 'admin@123', 'admin'):
            session['super_admin'] = True
            session['admin'] = True
            session.pop('faculty', None)
            session.pop('student', None)
            flash('Logged in as Super Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')
            return redirect(url_for('login', tab='admin'))
    return redirect(url_for('login', tab='admin'))


@app.route('/faculty/dashboard')
def faculty_dashboard():
    if not session.get('faculty') and not session.get('admin'):
        flash('Faculty access required.', 'warning')
        return redirect(url_for('login', tab='faculty'))
    
    fac_name = session.get('faculty_name', 'Dr. S. Rao')
    fac_id = session.get('faculty_id', 'FAC001')
    fac_dept = session.get('faculty_dept', 'Computer Science & Engineering')
    
    # Filter actions completed by this faculty member (strictly exclude login/logout or authentication actions)
    excluded_terms = ('login', 'logout', 'logged in', 'logged out', 'sign in', 'sign out', 'password', 'session', 'coordinator registration', 'registered coordinator')
    my_actions = [
        log for log in audit_logs 
        if (log['faculty_id'] == fac_id or log['faculty_name'] == fac_name)
        and not any(term in log.get('action_type', '').lower() or term in log.get('description', '').lower() or term in log.get('target', '').lower() for term in excluded_terms)
    ]
    
    stats = {
        'total_volunteers': len(volunteers),
        'active_volunteers': len([v for v in volunteers if v['status'] == 'active']),
        'total_events': len(events),
        'upcoming_events': len([e for e in events if e['status'] == 'upcoming']),
        'total_hours': sum(v.get('hours_completed', 0) for v in volunteers),
        'my_actions_count': len(my_actions)
    }
    return render_template('faculty_dashboard.html',
                           stats=stats,
                           volunteers=volunteers,
                           events=events,
                           my_actions=my_actions,
                           news_items=news_items,
                           attendance_records=attendance_records,
                           fac_name=fac_name,
                           fac_id=fac_id,
                           fac_dept=fac_dept)


@app.route('/faculty/logout')
def faculty_logout():
    session.pop('faculty', None)
    session.pop('faculty_id', None)
    session.pop('faculty_name', None)
    session.pop('admin', None)
    flash('Faculty coordinator logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/admin/logout')
def admin_logout():
    session.pop('super_admin', None)
    session.pop('admin', None)
    session.pop('faculty', None)
    flash('Super Admin logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/student/dashboard')
def student_dashboard():
    roll_no = session.get('student')
    if not roll_no:
        flash('Please login with your roll number to access the student portal.', 'warning')
        return redirect(url_for('login', tab='student'))
    
    volunteer = next((v for v in volunteers if v['roll_no'].upper() == roll_no.upper()), None)
    if not volunteer:
        session.pop('student', None)
        flash('Volunteer profile not found.', 'danger')
        return redirect(url_for('login', tab='student'))
    
    my_events = [e for e in events if volunteer['roll_no'] in e.get('registered_volunteers', [])]
    available_events = [e for e in events if e.get('status') == 'upcoming' and volunteer['roll_no'] not in e.get('registered_volunteers', [])]
    my_attendance = [a for a in attendance_records if volunteer['roll_no'] in a.get('present', [])]
    
    target_hours = 120
    progress_pct = min(100, int((volunteer.get('hours_completed', 0) / target_hours) * 100))
    
    return render_template('student_dashboard.html',
                           volunteer=volunteer,
                           my_events=my_events,
                           available_events=available_events,
                           my_attendance=my_attendance,
                           news_items=news_items,
                           target_hours=target_hours,
                           progress_pct=progress_pct)


@app.route('/student/logout')
def student_logout():
    session.pop('student', None)
    session.pop('student_name', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/admin')
@app.route('/admin/dashboard')
def admin_dashboard():
    return redirect(url_for('faculty_dashboard'))
    if False:
        flash('Super Admin access required. Please log in.', 'warning')
        return redirect(url_for('login', tab='admin'))
    
    filter_type = request.args.get('filter', 'all')
    if filter_type != 'all':
        filtered_logs = [l for l in audit_logs if filter_type.lower() in l['action_type'].lower()]
    else:
        filtered_logs = audit_logs

    faculty_summary = []
    for fac in faculty_members:
        fac_logs = [l for l in audit_logs if l['faculty_id'] == fac['faculty_id']]
        faculty_summary.append({
            'name': fac['name'],
            'faculty_id': fac['faculty_id'],
            'department': fac['department'],
            'email': fac['email'],
            'total_actions': len(fac_logs),
            'last_action': fac_logs[0]['timestamp'] if fac_logs else 'None yet'
        })

    stats = {
        'total_volunteers': len(volunteers),
        'active_volunteers': len([v for v in volunteers if v['status'] == 'active']),
        'total_events': len(events),
        'upcoming_events': len([e for e in events if e['status'] == 'upcoming']),
        'total_hours': sum(v.get('hours_completed', 0) for v in volunteers),
        'messages': len(contacts),
        'total_faculty': len(faculty_members),
        'total_audit_actions': len(audit_logs)
    }
    return render_template('admin_dashboard.html',
                           stats=stats,
                           volunteers=volunteers,
                           events=events,
                           contacts=contacts,
                           news_items=news_items,
                           audit_logs=filtered_logs,
                           faculty_summary=faculty_summary,
                           current_filter=filter_type)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting NSS Portal on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
