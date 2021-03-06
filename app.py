from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# configure the database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


# blog post model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return 'Blog post ' + str(self.id)


# dummy posts list
all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of the post',
        'author': 'Jane'
    },
    {
        'title': 'Post 2',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Assumenda dolor doloremque velit voluptatibus. Ad, aut consequatur cumque, doloremque eius fugiat fugit iste iusto magnam minima nobis nulla officia perferendis repudiandae.'
    }
]

# Get the home page
@app.route('/')
def index():
    return render_template('index.html')


# Displays all posts
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        # get post title
        title = request.form['title']
        # get post content
        content = request.form['content']
        # get the author
        author = request.form['author']
        # create post
        post = BlogPost(title=title, content=content, author=author)
        # add to session
        db.session.add(post)
        # save to db
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.created_at).all()
    return render_template('posts.html', posts=all_posts)


# shows page for creating post
@app.route('/posts/create')
def create():
    return render_template('create.html')


# Delete a post
@app.route('/posts/delete/<int:id>')
def post(id):
    # get the post
    post = BlogPost.query.get_or_404(id)
    # delete from session
    db.session.delete(post)
    # delete from db
    db.session.commit()
    return redirect('/posts')

# Edit a post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # get the post from the database
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        # get post title
        post.title = request.form['title']
        # get post content
        post.content = request.form['content']
        # get the author
        post.author = request.form['author']
        # add to session
        db.session.add(post)
        # save to db
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
