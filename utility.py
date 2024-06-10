def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "date_joined": user.date_joined
    }


def post_to_dict(post):
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "user_id": post.user_id,
        "categroy": post.category,
        "date_created": post.date_created
    }


def user_details_to_dict(user_details):
    return {
        "id": user_details.id,
        "address": user_details.address,
        "user_id": user_details.id,
        "bio": user_details.bio,
        "date_of_birth": user_details.date_of_birth
    } 

def image_to_dict(image):
    return {
        "id": image.id,
        "img": str(image.img),
        "name": image.name,
        "mimetype": image.mimetype,
        "post_id": image.post_id,
        "user_detail": image.user_detail_id
    }   

