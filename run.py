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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

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
    music_data = db.Column(db.BLOB)


@app.route('/', methods=['POST', 'GET'])
def music():
    page = request.args.get('page', 1, type=int)
    form = UploadMusic()
    if form.is_submitted():
        file = request.files['music']
        music_file = save_img(form.music.data)
        post = Music(music_data=file.read(),
                     music_filename=music_file)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('music'))
    posts = Music.query.filter_by(music_filename=Music.music_filename).order_by(
        Music.music_filename.desc()).paginate(page=page, per_page=10)
    #x = random.shuffle(posts)

    return render_template('music.html', form=form, posts=posts)


if __name__ == ('__main__'):
    app.run(debug=True, port=2348)
