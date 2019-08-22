from typing import Dict, Any, List

from django.contrib.auth import authenticate

from blog.models import User, Post, Comment
from django.contrib.auth.models import User as DjangoUser


def get_serialized_user(uuid: str) -> Dict[str, Any]:
    user = User.objects.get(id=uuid)

    user_dict = user.to_dict()
    for post in user.post_set.all():
        post_dict = post.to_dict()
        for comment in post.comment_set.all():
            post_dict['comments'].append(comment.to_dict())
        user_dict['posts'].append(post_dict)

    return user_dict


def subscribe(user: str, subscriber: str) -> bool:
    if user == '' or subscriber == '':
        return False
    find_user = User.objects.get(id=user)
    find_subscriber = User.objects.get(id=subscriber)
    find_user.subscribers.add(find_subscriber)
    find_subscriber.subscribes.add(find_user)
    find_subscriber.save()
    find_user.save()
    return True


def unsubscribe(user: str, subscriber: str) -> bool:
    if user == '' or subscriber == '':
        return False
    find_user = User.objects.get(id=user)
    find_subscriber = User.objects.get(id=subscriber)
    find_subscriber.subscribes.remove(find_user)
    find_user.subscribers.remove(find_subscriber)
    find_subscriber.save()
    find_user.save()
    return True


def get_all_subscriptions(uuid: str) -> List[Dict[str, Any]]:
    user = User.objects.get(id=uuid)
    users_dict: List[Dict[str, Any]] = [get_serialized_user(i.id) for i in user.subscribes.all()]
    return users_dict


def delete_user(uuid: str, password: str) -> bool:
    user = User.objects.get(id=uuid)
    user.password = password
    if is_user_authenticated(user):
        user.delete()
        return True
    return False


def get_user(uuid: str) -> User:
    return User.objects.get(id=uuid)


def create_user(user: User) -> bool:
    if user.is_valid():
        if user.is_authorized:
            if user.password is not None:
                user.save()
                django_user = DjangoUser.objects.create_user(user.name, user.password)
                # чтобы проверять, одинаковые ли пользователи
                django_user.first_name = user.id
                django_user.save()
                return True
    return False


def update_user(user: User) -> bool:
    if is_user_authenticated(user):
        user.save()
        return True
    return False


def create_post(post: Post, user_password: str) -> bool:
    author = post.author
    if is_user_authenticated(author, user_password):
        post.save()
        return True
    return False


def get_post(post_id: int) -> Post:
    return Post.objects.get(id=post_id)


def delete_post(post_id: int, user_password: str) -> bool:
    user_post = Post.objects.get(id=post_id)
    user = user_post.author
    user.password = user_password
    if is_user_authenticated(user):
        user_post.delete()
        return True
    return False


def create_comment(comment: Comment, user_password: str) -> bool:
    if is_user_authenticated(comment.author, user_password):
        comment.save()
        return True
    return False


def delete_comment(identity: int, user_password: str) -> bool:
    user_comment = Comment.objects.get(id=identity)
    user = user_comment.author
    user.password = user_password
    if is_user_authenticated(user, user_password):
        user_comment.delete()
        return True
    return False


def get_comment(comment_identity: int) -> Comment:
    return Comment.objects.get(id=comment_identity)


# util function
def is_user_authenticated(user: User, user_password: str = None) -> bool:
    if user.is_valid():
        if user_password is not None:
            authenticated_user = authenticate(user.name, password=user_password)
            if authenticated_user is not None and authenticated_user.first_name == user.id:
                return True
        if user.password is not None:
            authenticated_user = authenticate(user.name, password=user.password)
            if authenticated_user is not None and authenticated_user.first_name == user.id:
                return True
    return False
