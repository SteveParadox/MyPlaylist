import random

from flask import *
from flask_sqlalchemy import SQLAlchemy
from form import *

app = Flask(__name__)
db = SQLAlchemy(app)
import os
import secrets
from flask import current_app

app.secret_key = 'asdnafnj#46sjsnvd(*$43sfjkndkjvnskb6441531@#$$6sddf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://isyrbsxhlmykke:264c21cf7c770bfbe586fdd4c413bebb6da3fa34f154a262d8dd73de2ea1d2a7@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d7ct20f1f2urjn'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


def save_img(form_photo):
    if form_photo:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_photo.filename)
        path = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/MyPlaylist', path)
        size = (625, 625)
        form_photo.save(picture_path)

        return path


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    music_filename = db.Column(db.String())
    music_data = db.Column(db.LargeBinary)


@app.route('/', methods=['POST', 'GET'])
def music():
    page = request.args.get('page', 1, type=int)
    form = UploadMusic()
    if form.is_submitted():
        file = request.files['music']
        filename = secure_filename(file.filename)
        music_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(music_file)
        post = Music(music_data=music_file, music_filename=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('music'))
    posts = Music.query.order_by(Music.date_created.desc()).paginate(page=page, per_page=10)
    return render_template('music.html', form=form, posts=posts)



if __name__ == ('__main__'):
    app.run(debug=True, port=2848)
