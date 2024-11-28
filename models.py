
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    event_type = db.Column(db.String(50), nullable=False)  # "festival", "regular", "birthday", "user-created"
    created_by_user = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Event {self.title} on {self.date}>'

if __name__ == "__main__":
    app.run(debug=True)
