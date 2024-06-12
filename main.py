from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, session, flash, jsonify
from werkzeug.utils import secure_filename 
from datetime import datetime
from base64 import b64encode
import base64
from flask_migrate import Migrate
from utility import user_to_dict, image_to_dict, post_to_dict
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foodBloggerDB.sqlite3"
app.secret_key = "secret key"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -------- Utility Functions -------- #

def limit_postlength(post):
    if len(post) > 100:
        shorted_post = post[:100]
        return f"{shorted_post}..."
    return post



def b64encode(value):
    return base64.b64encode(value).decode('utf-8')

app.jinja_env.filters['b64encode'] = b64encode

# -------- Utility Functions -------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.Date, default=datetime.now())
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    address = db.Column(db.String(100))
    bio = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    image = db.relationship("Image", backref="user", cascade="all, delete-orphan", uselist=False)

    def __repr__(self) -> str:
        return f"<ID: {self.id} Name: {self.name} Email: {self.email}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    image = db.relationship("Image", backref="post", cascade="all, delete-orphan")
    category = db.Column(db.String(50), default="Breakfast")
    date_created = db.Column(db.Date, default=datetime.now())
     
    def __repr__(self) -> str:
        return f"<ID: {self.id} Title: {self.title} Body: {self.body} User ID: {self.user_id}"

# class UserDetail(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(100))
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     bio = db.Column(db.Text)
#     date_of_birth = db.Column(db.Date)

#     def __repr__(self) -> str:
#         return f"<ID: {self.id} Name:{self.user_id} Mimetype: {self.date_of_birth}"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", name="fk_image_post_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_image_user_id"))

    def __repr__(self) -> str:
        return f"<ID: {self.id} Name:{self.name} Mimetype: {self.mimetype} Data: {self.img}"



# class User_Image(db.Model):
#     pass

@app.route("/", methods=["GET"])
def root():
    """Routes user to root page and displays all user posts
    GET: returns 200"""
    posts = Post.query.all()
    post_list = []



    for post in posts:
        post_list.append(post_to_dict(post))


    return (jsonify(posts=post_list), 200)


@app.route("/get_posts_by_user_id/<user_id>", methods=["GET"])
def get_posts_by_user_id(user_id):
    """Returns 200 if posts found, else 404"""
    posts = Post.query.filter(Post.user_id == user_id).all()
    post_list = []
    # If user has no posts
    if not posts:
        return (jsonify({"response": "Not found Error"}), 404)
    

    for post in posts:
        post_list.append(post_to_dict(post))

    return (jsonify(posts=post_list), 200)

@app.route("/get_post_by_id/<post_id>", methods=["GET"])
def get_post_by_id(post_id):
    """Returns post and 200 if post exists else 404"""
    post = Post.query.filter(Post.id == post_id).first()

    # If post at id does not exist
    if not post:
        return jsonify({"response": "Not Found Error"}, 404)
    # If post at id exists
    return (jsonify(post=post_to_dict(post)), 200)

@app.route("/get_user_by_id/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """Returns user and 200 if user exists else 404"""
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return (jsonify({"response": "Not Found Error"}), 404)
    return (jsonify(user_to_dict(user)), 200)

@app.route("/get_all_users", methods=["GET"])
def get_all_users():
    """Returns all users and 200 if users exist else 404"""
    users = User.query.all()

    if not users:
        return (jsonify({"response": "Not Found Error"}), 404)
    
    # Parse SQL_Alchemy objects into python dictionary data types
    user_list = []
    for user in users:
        user_list.append(user_to_dict(user))
    return (jsonify(users=user_list), 200)

@app.route("/get_all_images", methods=["GET"])
def get_all_images(): 
    """Returns all images and 200 if images exist else 404"""
    images = Image.query.all()

    # Returns 404 if there are no images
    if not images:
        return (jsonify({"response": "Not Found Error"}), 404)
    
    # Parses SQL Alchemy Image object to Python dictionary data type
    image_list = [image_to_dict(image) for image in images]
    return (jsonify(images=image_list), 200)

@app.route("/get_images_by_post_id/<post_id>", methods=["GET"])
def get_images_by_post_id(post_id): 
    """Returns post images and 200 if post images exist else 404"""
    images = Image.query.filter(Image.post_id == post_id).all()

    # Returns 404 if post has no images
    if not images:
        return (jsonify({"response": "Not Found Error"}), 404)
    
    # Parses SQL Alchemy Image object to Python dictionary data type
    image_list = [image_to_dict(image) for image in images]
    return (jsonify(images=image_list), 200)

@app.route("/get_image_by_id/<image_id>", methods=["GET"])
def get_image_by_id(image_id): 
    """Returns all images and 200 if images exist else 404"""
    image = Image.query.filter(Image.id == image_id).first()

    # Returns 404 if image does not exist
    if not image:
        return (jsonify({"response": "Not Found Error"}), 404)
    return (jsonify(image=image_to_dict(image)), 200)

@app.route("/create_user", methods=["POST"])
def create_user():
    """Creates a new user from JSON input and returns its data"""
    data = request.get_json()  # Parse JSON data from request body

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    # Extract data from the JSON payload
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    date_of_birth = data.get("date_of_birth")
    address = data.get("address")
    bio = data.get("bio")
    profile_image_data = data.get("profile_image")  # Assuming image data is sent as base64 string or URL

    if not all([name, email, password, date_of_birth, address, bio]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create User and UserDetail instances
    date_object = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    user = User(name=name, email=email, password=password, address=address, bio=bio, date_of_birth=date_object)
    # Save user and user detail to the database
    db.session.add(user)
    db.session.commit()

    # Handle profile image if provided
    if profile_image_data:
        profile_image = Image(img=profile_image_data, mimetype='image/jpeg', name=f"{user.id}_profile.jpg", user=user)
        db.session.add(profile_image)
        db.session.commit()

    return jsonify(user=user_to_dict(user)), 201

@app.route("/create_post/<user_id>", methods=["POST"])
def create_post(user_id):
    """Creates a new post from JSON input and returns its data and 201"""
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return (jsonify({"error": "User Not Found"}), 404)

    data = request.get_json()
    if not data:
        return (jsonify({"error": "No Input Detected"}), 400)   # Parse JSON data from request body

    # Extract data from the JSON payload
    try: 
        title = data.get("title")
        body = data.get("body")
        category = data.get("category")
        post_image_b64 = data.get("post_image")
    except AttributeError:
        return (jsonify({"error": "Invalid JSON Input Detected"}), 400)

    if not all([title, body, category]):
        return (jsonify({"error": "Missing required fields"}), 400)

    post = Post(title=title, body=body, category=category, user=user)
    # Save post to the database
    db.session.add(post)
    db.session.commit()

    # Handle profile image if provided
    if post_image_b64:
        post_image = Image(img=post_image_b64, mimetype='image/jpeg', name=f"{post.id}_post.jpg", post=post)
        db.session.add(post_image)
        db.session.commit()

    return (jsonify(post=post_to_dict(post)), 201)

@app.route("/edit_post/<post_id>", methods=["PUT"])
def edit_post(post_id):
    """Edits post from corresponding ID, returns (post with 201 if PUT succesful), 
    (404 if post not found), (400 if invalid data is input or a field is missing)"""
    post = Post.query.filter(Post.id == post_id).first()
    
    # Check if post exists
    if not post:
        return (jsonify({"error": "Post Not Found"}), 404)

    data = request.get_json()  # Parse JSON data from request body

    # Checks if post entered input
    if not data:
        return (jsonify({"error": "Invalid input"}), 400)

    # Extract data from the JSON payload
    title = data.get("title")
    body = data.get("body")
    category = data.get("category")


    if not all([title, body, category]):
        return jsonify({"error": "Missing required fields"}), 400


    post.title = title
    post.body = body
    post.category = category
    
    db.session.commit() # Save user to the database
    return jsonify(user=post_to_dict(post)), 201

@app.route("/delete_user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Returns 200 if user deleted successfully or 404 if user not found"""
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return (jsonify({"response": "User Not Found"}), 404) # Checks if user exists

    db.session.delete(user)
    db.session.commit()

    return (jsonify({"response": "User deleted succesfully"}), 200)



@app.route("/delete_image/<image_id>", methods=["DELETE"])
def delete_image(image_id):
    """Returns 200 if image deleted successfully or 404 if user not found"""
    image = Image.query.filter(Image.id == image_id).first()

    if not image:
        return (jsonify({"response": "Image Not Found"}), 404) # Checks if image exists

    db.session.delete(image)
    db.session.commit()

    return (jsonify({"response": "Image deleted succesfully"}), 200)


@app.route("/delete_post/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    """Returns 200 if user deleted successfully or 404 if user not found"""
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return (jsonify({"response": "Post Not Found"}), 404) # Checks if post exists

    db.session.delete(post)
    db.session.commit()

    return (jsonify({"response": "Post deleted succesfully"}), 200)



@app.errorhandler(404)
def not_found_error(error):
    """Routes post to 404.html if a non existing route is entered"""

    return jsonify({"response": "Not Found Error"}), 404

@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({"response": "Internal Server Errror"}), 500

@app.errorhandler(415)
def unsupported_media_type(error):

    return jsonify({"response": "Unsupported Media Type"}), 415


# with app.app_context():
#     db.drop_all()
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)





# TODO Combine user_details and user into a single table and set a foreign key in users
# TODO Add feature to test one endpoint
# TODO MAJOR REFACTORING OF ALL ROUTES TO RETURN HTTP RESPONSE OR JSON DATA
# TODO Create dictionary parsing functions as utilities for returning JSON DATA

# ----- Bugs ----- #
"""Bug: input/textarea tags for (signup,new_post,edit_post) allow strings of unending single line characters"""
# ----- Bugs ----- #



# ----- Fixed Bugs ----- #

"""Bug: edit_post route template's title input value will not return the current title value correctly"""

# ----- Fixed Bugs ----- #
# ----- DONE TODOS ----- #
# TODO  Add flash messages
# TODO Add form validation
# TODO 1 Add 2 new column feilds to user: description, user_image-backref
# TODO 2 Modifiy constraint on user table column post-backref: Add cascade(delete orphan) constraint
# TODO Add feature to let user delete a post and image
# TODO Add user image(optional) and user description(optional) columns
# TODO  Paraphrase the template default posts in the database
# TODO Add feature which lets users view other viewers profiles by clicking on the name of a post

# ----- DONE TODOS ----- #


