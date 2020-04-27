from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class UploadMusic(FlaskForm):
    music = FileField('Upload Music', validators=[FileAllowed(['mp3']), DataRequired()])
    submit = SubmitField('Upload')
