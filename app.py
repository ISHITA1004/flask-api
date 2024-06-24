from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Video {self.id}: {self.title}>'


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# GET all videos
@app.route('/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    video_list = []
    for video in videos:
        video_dict = {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'url': video.url
        }
        video_list.append(video_dict)
    return jsonify(video_list)

# GET a specific video by ID
@app.route('/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    video_dict = {
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'url': video.url
    }
    return jsonify(video_dict)

# POST create a new video
@app.route('/videos', methods=['POST'])
def create_video():
    if not request.json or not 'title' in request.json or not 'url' in request.json:
        abort(400, description="Invalid JSON data")

    new_video = Video(
        title=request.json['title'],
        description=request.json.get('description', ""),
        url=request.json['url']
    )

    db.session.add(new_video)
    db.session.commit()

    return jsonify({
        'id': new_video.id,
        'title': new_video.title,
        'description': new_video.description,
        'url': new_video.url
    }), 201

# PUT update an existing video
@app.route('/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    video = Video.query.get_or_404(video_id)

    if not request.json:
        abort(400, description="Invalid JSON data")

    if 'title' in request.json:
        video.title = request.json['title']
    if 'description' in request.json:
        video.description = request.json['description']
    if 'url' in request.json:
        video.url = request.json['url']

    db.session.commit()

    return jsonify({
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'url': video.url
    })

# DELETE a video
@app.route('/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)

    db.session.delete(video)
    db.session.commit()

    return jsonify({"message": f"Video with ID {video_id} has been deleted"})

if __name__ == '__main__':
    app.run(debug=True)
