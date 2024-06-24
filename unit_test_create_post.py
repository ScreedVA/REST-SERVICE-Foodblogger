from main import app, db, Post, User
import unittest




class FlaskTestCase(unittest.TestCase):
    """Will test create_post route on User with a user name of TestUser1
    In the case that TestUser1 is not availibe in the Database please create one through the create_user route 
    through the application"""
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            self.user_id = User.query.filter(User.name == "TestUser1").first_or_404().id
            db.create_all()

        

    def tearDown(self):
        with app.app_context():
            posts = Post.query.filter(Post.user_id == self.user_id).all()
            for post in posts:
                db.session.delete(post)
                db.session.commit()
    
    def test_create_post_route(self):
        data = {
            "title": "I had breakfast today",
            "body": "It was good",
            "category": "Breakfast"
        }
        response = self.app.post(f"/create_post/{self.user_id}", json=data)
        print("\n---------- TEST WITH VALID DATA ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 201)

    def test_with_no_title_field(self):
        data = {
            "body": "It was good",
            "category": "Breakfast"
        }
        response = self.app.post(f"/create_post/{self.user_id}", json=data)
        print("\n---------- TEST WITH NO TITLE FIELD ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 400)

    def test_with_no_body_field(self):
        data = {
            "title": "I had breakfast today",
            "category": "Breakfast"
        }
        response = self.app.post(f"/create_post/{self.user_id}", json=data)
        print("\n---------- TEST WITH NO BODY FIELD ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 400)

    def test_with_no_category_field(self):
        data = {
            "title": "I had breakfast today",
            "body": "It was good"
        }
        response = self.app.post(f"/create_post/{self.user_id}", json=data)
        print("\n---------- TEST WITH NO CATEGORY FIELD ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 400)
    
    def test_with_invalid_user(self):
        data = {
            "title": "I had breakfast today",
            "body": "It was good",
            "category": "Breakfast"
        }
        invalid_user_id = -1
        response = self.app.post(f"/create_post/{invalid_user_id}", json=data)
        print("\n---------- TEST WITH INVALID USER ID ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 404)

    def test_with_no_user(self):
        data = {
            "title": "I had breakfast today",
            "body": "It was good",
            "category": "Breakfast"
        }
        response = self.app.post(f"/create_post", json=data)
        print("\n---------- TEST WITH NO USER ID ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 404)


    def test_with_special_characters_in_fields(self):
        data = {
            "title": "!§&$/%(§%)§%§%=&)/$I had breakfast today!§&$/%(§%)§%§%=&)/$",
            "body": "!§&$/%(§%)§%§%=&)/$It was good!§&$/%(§%)§%§%=&)/$",
            "category": "!§&$/%(§%)§%§%=&)/$Breakfast!§&$/%(§%)§%§%=&)/$"
        }
        response = self.app.post(f"/create_post/{self.user_id}", json=data)
        print("\n---------- TEST WITH SPECIAL CHARACTERS IN FIELDS ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 201)

    def test_with_invalid_data(self):
        invalid_data = [
            {
            "title": "I had breakfast today!",
            "body": "It was good",
            "category": "Breakfast"
            }
        ]
        response = self.app.post(f"/create_post/{self.user_id}", json=invalid_data)
        print("\n---------- TEST WITH INVALID DATA ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 400)

    def test_with_no_data(self):
        response = self.app.post(f"/create_post/{self.user_id}", json=None)
        print("\n---------- TEST WITH NO DATA ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 415)

    def test_with_invalid_fields(self):
        invalid_title = True
        invalid_body = 123
        invalid_category = None
        response = self.app.post(f"/create_post/{self.user_id}", json={"title": invalid_title, "body": invalid_body, "category": invalid_category})
        print("\n---------- TEST WITH INVALID FIELDS ----------\n")
        print(f"Response Code: {response.status_code}\nResponse: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 400)
        




if __name__ == "__main__":
    unittest.main()