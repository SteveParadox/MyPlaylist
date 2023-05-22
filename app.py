import os
import secrets
from flask import Flask, render_template, redirect, request, current_app, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/MyPlaylist'

db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    music_filename = db.Column(db.String())
    music_data = db.Column(db.LargeBinary)

    def save(self):
        db.session.add(self)
        db.session.commit()


def save_file(form_file):
    if form_file:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_file.filename)
        filename = random_hex + f_ext
        file_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename)
        form_file.save(file_path)
        return filename


@app.route('/', methods=['POST', 'GET'])
def music():
    page = request.args.get('page', 1, type=int)
    form = UploadMusic()
    
    if form.validate_on_submit():
        file = form.music.data
        filename = secure_filename(file.filename)
        music_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        saved_filename = save_file(file)
        if saved_filename:
            post = Music(music_data=saved_filename, music_filename=filename)
            post.save()
            return redirect(url_for('music'))
    
    posts = Music.query.order_by(Music.id.desc()).paginate(page=page, per_page=10)
    return render_template('music.html', form=form, posts=posts)


if __name__ == '__main__':
    app.run(debug=True, port=2848)

