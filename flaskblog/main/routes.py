from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    # get the page param
    page = request.args.get('page', 1, type=int)
    # paginate the query for posts for the current page and the amount to show, 5 per page.
    # this returns an object with the items and other methods
    # passing page=page fills the items property of this paginate object
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

