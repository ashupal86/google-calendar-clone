from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # Change if using a different DB
app.config['SECRET_KEY'] = 'your_secret_key'  # Flash messages secret key
db = SQLAlchemy(app)

# Models
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Changed to Date type for better handling
    event_type = db.Column(db.String(50), nullable=False)
    created_by_user = db.Column(db.Boolean, default=False)

    def __init__(self, title, date, event_type, created_by_user=False):
        self.title = title
        self.date = date
        self.event_type = event_type
        self.created_by_user = created_by_user

    def __repr__(self):
        return f"<Event {self.title} on {self.date}>"

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    today = datetime.today().date()
    month_start = today.replace(day=1)
    next_month_start = (month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1))
    month_end = next_month_start - timedelta(days=1)

    # Get events for the current month
    events = Event.query.filter(Event.date >= month_start, Event.date <= month_end).all()

    # Split events by types
    festivals = [{"e_date": event.date.strftime('%d'), "e_title": event.title, "e_type": event.event_type} for event in events if event.event_type == 'festival']
    user_created_events = [{"e_date": event.date.strftime('%d'), "e_title": event.title, "e_type": event.event_type} for event in events if event.created_by_user]
    birthday_events = [{"e_date": event.date.strftime('%d'), "e_title": event.title, "e_type": event.event_type} for event in events if event.event_type == 'birthday']
    regular_events = [{"e_date": event.date.strftime('%d'), "e_title": event.title, "e_type": event.event_type} for event in events if event.event_type == 'regular']

    # Get today's events
    todays_events = [event for event in events if event.date == today]

    # Generate the calendar for the month
    month_calendar = generate_month_calendar(month_start)
    dates = [e_date for e_date in festivals  + birthday_events + regular_events]
    

    return render_template('index.html',
                           today=today,
                           month_calendar=month_calendar,
                           festivals=festivals,
                           user_created_events=user_created_events,
                           birthday_events=birthday_events,
                           regular_events=regular_events,
                           todays_events=todays_events,
                           dates=dates,
                           events=events
                           )
                           

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form['title']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    event_type = request.form['event_type']
    created_by_user = request.form.get('created_by_user') == 'on'  # Checkbox for user-created events

    new_event = Event(title=title, date=date, event_type=event_type, created_by_user=created_by_user)

    db.session.add(new_event)
    db.session.commit()

    flash('Event added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        event.title = request.form['title']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.event_type = request.form['event_type']
        event.created_by_user = request.form.get('created_by_user') == 'on'

        db.session.commit()

        flash('Event updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_event.html', event=event)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()

    flash('Event deleted successfully!', 'success')
    return redirect(url_for('index'))

def generate_month_calendar(start_date):
    """ Generate the month calendar with dates divided by weeks """
    # Find the first and last day of the month
    first_day_of_month = start_date
    last_day_of_month = (first_day_of_month.replace(month=first_day_of_month.month + 1)
                          if first_day_of_month.month < 12
                          else first_day_of_month.replace(year=first_day_of_month.year + 1, month=1)) - timedelta(days=1)

    # Generate the calendar days, adjusting for the first day of the month
    first_day_of_week = first_day_of_month.weekday()  # Monday = 0, Sunday = 6
    calendar = []
    current_day = 1

    for week in range(6):  # Max of 6 weeks in a month
        week_days = []
        for day in range(7):
            if week == 0 and day < first_day_of_week:
                week_days.append(0)  # Empty cell before first day
            elif current_day > last_day_of_month.day:
                week_days.append(0)  # Empty cell after the last day of the month
            else:
                week_days.append(current_day)
                current_day += 1
        calendar.append(week_days)

    return calendar

if __name__ == '__main__':
    app.run(debug=True)