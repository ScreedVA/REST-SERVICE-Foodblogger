from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, session, flash, jsonify
from werkzeug.utils import secure_filename 
from datetime import datetime
from base64 import b64encode
import base64
from flask_migrate import Migrate
from utility import user_to_dict, user_details_to_dict, image_to_dict, post_to_dict
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
    user_detail = db.relationship("UserDetail", backref="user", cascade="all, delete-orphan", uselist=False)

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

class UserDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bio = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    image = db.relationship("Image", backref="user_detail", cascade="all, delete-orphan", uselist=False)

    def __repr__(self) -> str:
        return f"<ID: {self.id} Name:{self.user_id} Mimetype: {self.date_of_birth}"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", name="fk_image_post_id"))
    user_detail_id = db.Column(db.Integer, db.ForeignKey("user_detail.id", name="fk_image_user_details_id"))

    def __repr__(self) -> str:
        return f"<ID: {self.id} Name:{self.name} Mimetype: {self.mimetype} Data: {self.img}"



# class User_Image(db.Model):
#     pass

@app.context_processor
def inject_global_variables():
    is_signed_in = session.get("is_signed_in", False)
    current_user_id = session.get("user_id", 10000)
    blog_filter = session.get("blog_filter", "No Filter")
    return dict(signed_in=is_signed_in, limit_postlength=limit_postlength, blog_filter=blog_filter, current_user_id=current_user_id)


@app.route("/", methods=["GET"])
def root():
    """Routes user to root page and displays all user posts
    GET: returns 200"""
    posts = Post.query.all()
    post_list = []

    for post in posts:
        post_list.append(post_to_dict(post))


    return jsonify(post_list), 200


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
    user = User(name=name, email=email, password=password)
    date_object = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    user_detail = UserDetail(address=address, date_of_birth=date_object, bio=bio, user=user)

    # Save user and user detail to the database
    db.session.add(user)
    db.session.add(user_detail)
    db.session.commit()

    # Handle profile image if provided
    if profile_image_data:
        profile_image = Image(img=profile_image_data, mimetype='image/jpeg', name=f"{user.id}_profile.jpg", user_detail=user_detail)
        db.session.add(profile_image)
        db.session.commit()

    # Prepare the response data
    new_user = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "date_of_birth": date_of_birth,
        "address": address,
        "bio": bio,
        "profile_image": profile_image_data  # Assuming you want to include this in the response
    }

    return jsonify(user=new_user), 201




@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """Routes use to sign_in.html page
    GET: returns 200
    POST: returns 200, redirects to user_gallery router"""
    users = User.query.all()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter(User.name == username).first()
        if user and user.password == password:
            print(user)

            session["is_signed_in"] = True
            session["user_id"] = user.id
            session["username"] = username
            flash(f"Welcome {user.name}", category="success")
            return redirect(url_for("user_gallery", user_id=user.id)) # 200 The request has suceeded, as the user_gallery router is returned.
        else:
            flash("Wrong password or username", category="danger")

    return (render_template("/user_temps/sign_in.html", users=users), 200) # The request has suceeded, as the sign_in.html page is returned.


@app.route("/user_gallery")
@app.route("/user_gallery/<user_id>")
def user_gallery(user_id):
    """Routes user to user_gallery.html page which includes buttons to route to edit_user, delete_user and make_post
    GET: returns 200"""
    # if "is_signed_in" in session and session["is_signed_in"]:
    # Checks if a user is signed in
    profile_image = None
    user = User.query.filter(User.id == user_id).first()
    posts = Post.query.filter(Post.user_id == user.id).all()        
    user_details = UserDetail.query.filter(UserDetail.user_id == user.id).first()
    if user_details:
        profile_image = Image.query.filter(Image.user_detail_id == user_details.id).first()
    return (render_template("user_temps/user_gallery.html", username=user.name, user=user, posts=posts, image_class=Image, profile_image=profile_image), 200) # 200 The request has suceeded, as the user_gallery.html page is returned.
    # return (render_template("user_temps/user_gallery.html", user=user,), 200) # 200 The request has suceeded, as the user_gallery.html page is returned.

@app.route("/select_user_profile_view/<user_id>")
def select_user_profile_view(user_id):
    """Routes user to user_profile_view.html page, which displays user's full details"""
    user = User.query.filter(User.id == user_id).first()
    user_detail = UserDetail.query.filter(UserDetail.user_id == user.id).first()
    post = Post.query.filter(Post.user_id == user_id).all()
    profile_image = Image.query.filter(Image.user_detail_id == user_detail.id).first()
    request_from = request.args.get("from_view")

    return (render_template("user_temps/select_user_profile_view.html", user=user, user_detail=user_detail, post=post, profile_image=profile_image, from_view=request_from), 200) # The request has suceeded, as the select_user_profile_view.html page is returned.

@app.route("/sign_out")
def sign_out():
    """Routes user back to root page
    GET: returns 200"""
    
    flash(f"Signed out of {session["username"]}", category="danger")
    session.pop("is_signed_in", None)
    session.pop("username", None)
    session.pop("user_id", None)

    return redirect(url_for("root")) # 200 The request has suceeded, as the root.html page is returned.

@app.route("/edit_user/<user_id>", methods=["GET", "POST", "PUT"])
def edit_user(user_id):
    """Routes user to edit_user.html where user can edit thier account details
    GET: returns 200
    POST: returns 201"""
    profile_image = None
    user = User.query.filter(User.id == user_id).first()
    user_detail = UserDetail.query.filter(UserDetail.user_id == user.id).first()
    if user_detail:
        profile_image = Image.query.filter(Image.user_detail_id == user_detail.id).first()
    if request.method == "POST" or request.method == "PUT":
        # Check if user submited the edit user form
        user.name = session["username"] = request.form["username"]
        user.email = request.form["email"]
        user.password = request.form["password"]
        user_detail.address = request.form["address"]
        user_detail.date_of_birth = datetime.strptime(request.form["date_of_birth"], '%Y-%m-%d').date()
        user_detail.bio = request.form["bio"]

        db.session.add(user)
        db.session.add(user_detail)
        db.session.commit()
        pic = request.files["profile_image"]
        if pic:
            # Check if user uploaded a new image
            if user_detail.image:
            # Check if User profile image already exists
                profile_image = Image.query.filter(Image.user_detail_id == user_detail.id).first()
                db.session.delete(profile_image)
                db.session.commit()
            new_profile_image = Image(img=pic.read(), mimetype=pic.mimetype, name=secure_filename(pic.filename), user_detail=user_detail)
            db.session.add(new_profile_image)
            db.session.commit()
        flash(f"{user.name} Has been edited", category="warning")
        return redirect(url_for("user_gallery", user_id=user_id)) # The 201 request has been fulfilled as new resources are being created 
    return render_template("/user_temps/edit_user.html", user=user, user_detail=user_detail, profile_image=profile_image) # The request has succeeded, as the edit_post.html page is returned


@app.route("/delete_user/<user_id>", methods=["GET", "DELETE"])
def delete_user(user_id):
    """Deletes current user when called
    DELETE: returns 200, redirects to root router"""
    user = User.query.filter(User.id == user_id).first()
    flash(f"{user.name} Has been deleted", category="danger")
    db.session.delete(user)
    db.session.commit()

    session.pop("is_signed_in", None)
    session.pop("username", None)
    session.pop("user_id", None)

    return redirect(url_for("root")) # The 200 request has succeeded, and the resource has been deleted



@app.route("/new_post/<user_id>", methods=["GET", "POST"])
def new_post(user_id):
    """Routes user to new_post.html page to publish a new post
    GET: returns 200
    POST: returns 201"""
    user = User.query.filter(User.id == user_id).first()
    if request.method == "POST":
        form_title = request.form["title"]
        form_body = request.form["body"]
        form_category = request.form.get("category")
        form_image = request.files["image"]
        post = Post(title=form_title, body=form_body, user=user, category=form_category)
        db.session.add(post)
        db.session.commit()
            
        if form_image:
            filename = secure_filename(form_image.filename)
            image = Image(img=form_image.read(), mimetype=form_image.mimetype, name=filename, post=post)
            db.session.add(image)
            db.session.commit()
        flash("Your post has been published", category="success")
        return redirect(url_for("select_post_view", post_id=post.id, from_view="user_gallery")) # The 201 request has been fulfilled as new resources are being created
    return (render_template("post_temps/new_post.html"), 200) # The request has suceeded, as the new_post.html page is returned.


@app.route("/delete_post/<post_id>", methods=["GET", "DELETE"])
def delete_post(post_id):
    """Deletes current post at post_id and routes to user_gallery.html
    DELETE: returns 200, redirects to user_gallery router"""
    flash("Post Deleted", category="danger")
    post = Post.query.filter(Post.id == post_id).first()
    user = User.query.filter(User.id == Post.user_id).first()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("user_gallery", user_id=user.id)) # The 200 request has succeeded, and the resource has been deleted

@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """Lets users edit posts, routes user to edit_post.htm, 
    GET: returns 200 
    POST: returns 201"""
    request_from = request.args.get("from_view")
    post = Post.query.filter(Post.id == post_id).first()
    print(post.title)
    if request.method == "POST":
        # Check if user is submiting edit post form
        form_title = request.form["title"]
        form_body = request.form["body"]
        form_category = request.form["category"]
        form_image = request.files["image"]
        if form_image:
            # Check if user uploaded a new post image
            filename = secure_filename(form_image.filename)
            image = Image(img=form_image.read(), mimetype=form_image.mimetype, name=filename, post=post)
            db.session.add(image)
            db.session.commit()
        post.title = form_title
        post.body = form_body
        post.category = form_category
        db.session.commit()
        flash("Post has been updated", category="info")
        return redirect(url_for("select_post_view", post_id=post.id, from_view=request_from)) # The 201 request has been fulfilled as new resources are being created 
    return render_template("post_temps/edit_post.html", post=post, from_view=request_from) # The request has suceeded, as the edit_post.html page is returned




@app.route("/select_post_view/<post_id>")
def select_post_view(post_id):
    """Routes user to select_post_view page where user can edit or delete current post
    GET: returns 200"""
    request_from = request.args.get("from_view")
    print(request_from)
    post = Post.query.filter(Post.id == post_id).first()
    user = User.query.filter(User.id == post.user_id).first()
    images = Image.query.filter(Image.post_id == post.id).all()
    profile_image = Image.query.filter(Image.user_detail_id == UserDetail.query.filter(UserDetail.user_id == user.id).first().id).first()
    return render_template("post_temps/select_post_view.html", post=post, user=user, images=images, from_view=request_from, profile_image=profile_image) # The request has succeeded, as the select_view_post.html page is returned

@app.route("/select_image_view/<image_id>", methods=["GET", "POST", "DELETE"])
def select_image_view(image_id):
    """Routes to select_image_view.html page where user can see a current image in full scale or delete image
    GET: returns 200,
    DELETE: returns 200"""
    request_from = request.args.get("from_view")
    image = Image.query.filter(Image.id == image_id).first()
    if not image or not image.post:
        return render_template("error_temps/500.html")
    post = Post.query.filter(Post.id == image.post_id).first()
    if request.method == "POST" or request.method == "DELETE":
        db.session.delete(image)
        db.session.commit()
        flash("Image has been deleted", category="danger")
        return redirect(url_for("select_post_view", post_id=post.id, from_view=request_from)) # The 200 request has succeeded, and the resource has been deleted
    return render_template("image_temps/select_image_view.html", from_view=request_from, image=image, post=post) # The 200 request has succeeded, as the select_view_post.html page is returned


@app.errorhandler(404)
def not_found_error(error):
    """Routes user to 404.html if a non existing route is entered"""

    return render_template("error_temps/404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):

    return render_template("error_temps/500.html"), 500


def new_post(title, body, category):
    user = User.query.filter(User.name == "TestUser0").first()
    post = Post(title=title, body=body, category=category, user=user)

    db.session.add(post)
    db.session.commit()
    print(f"-- Post added to Database for {user.name} --\n")

def unit_test_new_post():
    print("\n----- Starting Unit Test -----\n\n")
    # Unit Test: Creating a new blog post with valid data
    print("Unit Test: Create a new blog post with valid data")
    new_post(title="Almond Cupcake with Raspberry Cheesecake Frosting", body="It tastes like springtime,” said Alana, our fabulous photographer, after her first bite of this creation. This cupcake was vying for top billing as well, and, depending on my mood, could steal the crown.",category="Dessert")

    # Unit Test: Create a new blog post with very long title
    print("Unit Test: Create a new blog post with very long title")
    new_post(title="Deliciously Decadent Almond Cupcake Infused with Rich Vanilla Extract, Topped with a Creamy Raspberry Cheesecake Frosting and Garnished with Freshly Picked Raspberries for a Burst of Summery Sweetness", body="It tastes like springtime,” said Alana, our fabulous photographer, after her first bite of this creation. This cupcake was vying for top billing as well, and, depending on my mood, could steal the crown.", category="Dessert")

    # Unit Test: Create a new blog post with very long body
    print("Unit Test: Create a new blog post with very long body")
    new_post(title="Almond Cupcake with Raspberry Cheesecake Frosting", body="It tastes like springtime,” said Alana, our fabulous photographer, after her first bite of this creation. This cupcake was vying for top billing as well, and, depending on my mood, could steal the crown. This cupcake was more delicate and dainty, where the cookie dough cupcake was bulkier, and more binge-eating worthy. The almond-flavored cake was delicious, and felt dense but not heavy. There was still a fluffiness to the cake, but there was enough body to make the small cupcake satisfying.This balance in baking is incredibly difficult — things tend to either be too fluffy and spongy, and feel like they will fall under the weight of heavy frosting, or they are so dense they feel solid and lose their spring. This was the perfect consistency. Occasionally crunching on raspberry seeds in the frosting was a pleasant reminder that it was the real deal. It was not overpoweringly fruity either, leaving a lot of the sugary, creamy cheesecake flavor to shine through, with the raspberry being the subtle top note. Together, this pairing was absolutely perfect. This would be a great cupcake for a high tea, a fancy dress birthday party with sparkling wines, or a super classy wedding that had a jazz band or orchestra for music instead of a DJ. That’s the feel of this cupcake. Sure, you can eat it on the couch in your sweatpants, but I feel like this cupcake deserves better", category="Dessert")

    # Unit Test: Create a new blog post with very short title
    print("Unit Test: Create a new blog post with very short title")
    new_post(title="Alm..", body="If you’ve read my reviews before, you will know that I am not a huge fan of lemon-flavored desserts. While I can appreciate them, they’re not my thing. That said, I do try and be objective in my reviews.", category="Dessert")

    # Unit Test: Create a new blog post with very short body
    print("Unit Test: Create a new blog post with very short body")
    new_post(title="Almond Cupcake with Raspberry Cheesecake Frosting", body="If you've...", category="Dessert")

    # Unit Test: Create a new blog post with empty title
    print("Unit Test: Create a new blog post with empty title")
    new_post(title="", body="If you’ve read my reviews before, you will know that I am not a huge fan of lemon-flavored desserts. While I can appreciate them, they’re not my thing. That said, I do try and be objective in my reviews.", category="Dessert")

    # Unit Test: Create a new Blog post with empty body
    print("Create a new blog post with empty body")
    new_post(title="Almond Cupcake with Raspberry Cheesecake Frosting", body="", category="Dessert")

    # Unit Test: Create a new blog post with an empty category
    print("Unit Test: Create a new blog post with an empty category")
    new_post(title="Almond Cupcake with Raspberry Cheesecake Frosting", body="If you’ve read my reviews before, you will know that I am not a huge fan of lemon-flavored desserts. While I can appreciate them, they’re not my thing. That said, I do try and be objective in my reviews.", category="")


    # Unit Test: Create a new blog post with special characters in title
    print("Unit Test: Create a new blog post with special characters in title")
    new_post(title="!§&$/%(§%)§%§%=&)/$Almond Cupcake with Raspberry Cheesecake Frosting!§&$/%(§%)§%§%=&)/$", body="If you’ve read my reviews before, you will know that I am not a huge fan of lemon-flavored desserts. While I can appreciate them, they’re not my thing. That said, I do try and be objective in my reviews.", category="Dessert")

    # Unit Test: Create a new blog post with special characters in catergory
    print("Unit Test: Create a new blog post with special characters in category")
    new_post(title="Almond Cupcake with Raspberry Cheesecake Frosting", body="If you’ve read my reviews before, you will know that I am not a huge fan of lemon-flavored desserts. While I can appreciate them, they’re not my thing. That said, I do try and be objective in my reviews.", category="!§&$/%(§%)§%§%=&)/$Dessert!§&$/%(§%)§%§%=&)/$")

    print("\n\n----- Ending Unit Test -----\n")


# with app.app_context():
#     unit_test_new_post()

if __name__ == "__main__":
    app.run(debug=True)
    # unit_test_new_post()
    pass






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


