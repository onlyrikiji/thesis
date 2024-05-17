from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title')
    hashtag = StringField('Hashtag')
    content = TextAreaField('Content', validators=[DataRequired()])
    sentiment = TextAreaField('Sentiment', render_kw={'readonly': True})
    submit = SubmitField('Post')
    analyze = SubmitField('Analyze') 

    
