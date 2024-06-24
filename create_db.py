from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Video {self.id}: {self.title}>'

# Create the database and tables
with app.app_context():
    db.create_all()

    # Seed the database with initial data
    if not Video.query.first():  # Check if the table is empty
        sample_videos = [
            Video(title='Sample Video 1', description='This is a sample video.', url='http://example.com/video1'),
            Video(title='Sample Video 2', description='This is another sample video.', url='http://example.com/video2')
        ]
        db.session.bulk_save_objects(sample_videos)
        db.session.commit()
