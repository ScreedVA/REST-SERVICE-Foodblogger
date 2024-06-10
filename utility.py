def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "date_joined": user.date_joined,
        "address": user.address,
        "bio": user.bio,
        "date_of_birth": user.date_of_birth
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

def image_to_dict(image):
    return {
        "id": image.id,
        "img": str(image.img),
        "name": image.name,
        "mimetype": image.mimetype,
        "post_id": image.post_id,
        "user_detail": image.user_detail_id
    }   

