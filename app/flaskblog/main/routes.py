from flask import render_template, request, Blueprint, current_app
from flaskblog.models import Post
import csv
import subprocess
 
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search_query', None, type=str)  # Get the search query from the query string

    if search_query:
        # Filter posts based on search query using regular expressions
        filtered_posts = Post.query.filter(Post.content.ilike(f'%{search_query}%')).paginate(page=page, per_page=5)

        # Log the search query to a CSV file
        with open('flaskblog/main/search_queries.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([search_query])

    else:
        filtered_posts = Post.query.paginate(page=page, per_page=5)

    return render_template('home.html', posts=filtered_posts)
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/run_script', methods=['GET'])
def run_script():
    script_path = "C:/Users/USER\Desktop/test_app2/flaskblog/main/quadall.py"
    subprocess.run(["python", script_path])
    return "Script executed successfully"


@main.route('/extra_action', methods=['GET'])
def extra_action_route():
    
    script_path = "C:/Users/USER/Desktop/test_app2/flaskblog/main/quad.py"
    subprocess.run(["python", script_path])
    
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search_query', None, type=str)
    
  # Get the search query from the query string
    if search_query:
        # Filter posts based on search query using regular expressions
        filtered_posts = Post.query.filter(Post.content.ilike(f'%{search_query}%')).paginate(page=page, per_page=5)
    else:
        filtered_posts = Post.query.paginate(page=page, per_page=5)

    return render_template('home.html', posts=filtered_posts)
