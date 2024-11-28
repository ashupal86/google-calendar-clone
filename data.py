from app import db, Event, app
from datetime import datetime, timedelta
import random

# Predefined Festival and Holiday Events
events_data = [
    {"title": "Republic Day", "date": "2024-01-26", "event_type": "festival", "created_by_user": False},
    {"title": "Holi", "date": "2024-03-25", "event_type": "festival", "created_by_user": False},
    {"title": "Good Friday", "date": "2024-03-29", "event_type": "festival", "created_by_user": False},
    {"title": "Eid al-Fitr", "date": "2024-04-10", "event_type": "festival", "created_by_user": False},
    {"title": "Independence Day", "date": "2024-08-15", "event_type": "festival", "created_by_user": False},
    {"title": "Raksha Bandhan", "date": "2024-08-19", "event_type": "festival", "created_by_user": False},
    {"title": "Ganesh Chaturthi", "date": "2024-09-07", "event_type": "festival", "created_by_user": False},
    {"title": "Gandhi Jayanti", "date": "2024-10-02", "event_type": "festival", "created_by_user": False},
    {"title": "Dussehra", "date": "2024-10-12", "event_type": "festival", "created_by_user": False},
    {"title": "Diwali", "date": "2024-11-01", "event_type": "festival", "created_by_user": False},
    {"title": "Christmas", "date": "2024-12-25", "event_type": "festival", "created_by_user": False},
    {"title": "Onam", "date": "2024-08-30", "event_type": "festival", "created_by_user": False},
    {"title": "Makar Sankranti", "date": "2024-01-14", "event_type": "festival", "created_by_user": False},
    {"title": "Baisakhi", "date": "2024-04-13", "event_type": "festival", "created_by_user": False},
    {"title": "Labour Day", "date": "2024-05-01", "event_type": "holiday", "created_by_user": False},
    {"title": "May Day", "date": "2024-05-01", "event_type": "holiday", "created_by_user": False},
    {"title": "International Yoga Day", "date": "2024-06-21", "event_type": "regular", "created_by_user": True},
    {"title": "World Environment Day", "date": "2024-06-05", "event_type": "regular", "created_by_user": True},
    {"title": "International Women's Day", "date": "2024-03-08", "event_type": "regular", "created_by_user": True},
    {"title": "National Sports Day", "date": "2024-08-29", "event_type": "regular", "created_by_user": True},
    {"title": "Teacher's Day", "date": "2024-09-05", "event_type": "regular", "created_by_user": True},
    {"title": "Children's Day", "date": "2024-11-14", "event_type": "regular", "created_by_user": True},
    {"title": "World Health Day", "date": "2024-04-07", "event_type": "regular", "created_by_user": True},
    {"title": "World Music Day", "date": "2024-06-21", "event_type": "regular", "created_by_user": True},
    {"title": "Mothers' Day", "date": "2024-05-12", "event_type": "regular", "created_by_user": True},
    {"title": "Fathers' Day", "date": "2024-06-16", "event_type": "regular", "created_by_user": True},
    {"title": "National Unity Day", "date": "2024-10-31", "event_type": "regular", "created_by_user": True},
    {"title": "World Tourism Day", "date": "2024-09-27", "event_type": "regular", "created_by_user": True},
    {"title": "National Day of India", "date": "2024-08-15", "event_type": "holiday", "created_by_user": False},
    {"title": "National Technology Day", "date": "2024-05-11", "event_type": "regular", "created_by_user": True},
    {"title": "National Farmers Day", "date": "2024-12-23", "event_type": "regular", "created_by_user": True},
    {"title": "National Army Day", "date": "2024-01-15", "event_type": "regular", "created_by_user": True},
    {"title": "National Flag Day", "date": "2024-12-07", "event_type": "regular", "created_by_user": True},
    {"title": "World Day for Cultural Diversity", "date": "2024-05-21", "event_type": "regular", "created_by_user": True},
    {"title": "World Red Cross Day", "date": "2024-05-08", "event_type": "regular", "created_by_user": True},
    {"title": "World Animal Day", "date": "2024-10-04", "event_type": "regular", "created_by_user": True},
    {"title": "World Day Against Child Labour", "date": "2024-06-12", "event_type": "regular", "created_by_user": True},
    {"title": "World Literacy Day", "date": "2024-09-08", "event_type": "regular", "created_by_user": True},
    {"title": "World Blood Donor Day", "date": "2024-06-14", "event_type": "regular", "created_by_user": True},
    {"title": "National Peace Day", "date": "2024-09-21", "event_type": "regular", "created_by_user": True},
    {"title": "National Women's Day", "date": "2024-08-09", "event_type": "regular", "created_by_user": True},
    {"title": "National Doctors' Day", "date": "2024-07-01", "event_type": "regular", "created_by_user": True},
    {"title": "National Handloom Day", "date": "2024-08-07", "event_type": "regular", "created_by_user": True},
    {"title": "National Maritime Day", "date": "2024-04-05", "event_type": "regular", "created_by_user": True},
    {"title": "World Health Organization Day", "date": "2024-04-07", "event_type": "regular", "created_by_user": True},
    {"title": "World Computer Literacy Day", "date": "2024-12-02", "event_type": "regular", "created_by_user": True},
    {"title": "World Television Day", "date": "2024-11-21", "event_type": "regular", "created_by_user": True},
    {"title": "International Day for Tolerance", "date": "2024-11-16", "event_type": "regular", "created_by_user": True},
    {"title": "World Food Day", "date": "2024-10-16", "event_type": "regular", "created_by_user": True},
    {"title": "World Mental Health Day", "date": "2024-10-10", "event_type": "regular", "created_by_user": True},
    {"title": "World Population Day", "date": "2024-07-11", "event_type": "regular", "created_by_user": True},
    {"title": "World Press Freedom Day", "date": "2024-05-03", "event_type": "regular", "created_by_user": True},
    {"title": "World International Day of Peace", "date": "2024-09-21", "event_type": "regular", "created_by_user": True},
    {"title": "National Handicapped Day", "date": "2024-12-03", "event_type": "regular", "created_by_user": True},
    {"title": "International Day of Charity", "date": "2024-09-05", "event_type": "regular", "created_by_user": True},
    {"title": "International Day for Disaster Reduction", "date": "2024-10-13", "event_type": "regular", "created_by_user": True},
]

# Insert events into the database
with app.app_context():
    with db.session.begin():
        for event in events_data:
            # Check if the event already exists in the database (to avoid duplicates)
            existing_event = Event.query.filter_by(title=event["title"], date=event["date"]).first()
            if not existing_event:
                # Correctly pass the attributes to match the Event constructor
                db.session.add(Event(
                    title=event["title"],
                    date=event["date"],
                    event_type=event["event_type"],
                    created_by_user=event["created_by_user"]
                ))

    # Commit changes to the database
    db.session.commit()

print("300 events added successfully!")
