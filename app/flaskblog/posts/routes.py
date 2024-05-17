from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
import requests
from dotenv import load_dotenv 
import os 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

posts = Blueprint('posts', __name__)

load_dotenv('.env')
api_url = os.environ.get('API_BASE_URL')
    
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    all_scores = []
    
    if form.validate_on_submit():
        if form.submit.data:
            # Get sentiment analysis result
            sentiment_data = {'text': form.content.data}
            response = requests.post(f"{api_url}/predict", json=sentiment_data)

            if response.status_code == 200:
                result = response.json()
                negative_score = float(result["negative"])
                # Determine sentiment based on polarity
                if negative_score is None:
                    sentiment = "Unknown"
                elif negative_score > 50:
                    sentiment = "Negative"
                elif negative_score < 0:
                    sentiment = "Postive"
                else:
                    sentiment = "Neutral"
                
                title=""
                hashtag=""
                # Create and save the post with sentiment
                post = Post(title=title, hashtag=hashtag, content=form.content.data, sentiment=sentiment, author=current_user)
                db.session.add(post)
                db.session.commit()
                
                flash('Your post has been created!', 'success')
                return redirect(url_for('main.home'))
            
        elif form.analyze.data:
            # Get sentiment analysis result
            sentiment_data = {'text': form.content.data}
            response = requests.post(f"{api_url}/predict", json=sentiment_data)
            
            
            if response.status_code == 200:
                data = response.json()
                all_scores = [float(value) for value in data.values()]
                
            if response.status_code == 200:
                result = response.json()
                emotions_above_50 = []

                # Check scores and store emotions above 50
                for emotion, score in result.items():
                    if float(score) > 50:
                        emotions_above_50.append(emotion)

                # Convert list of emotions to a comma-separated string
                emotions_string = ", ".join(emotions_above_50)
            
                form.sentiment.data = emotions_string
                flash('Analyze Success!', 'success')
            
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post', all_scores=all_scores)




@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


