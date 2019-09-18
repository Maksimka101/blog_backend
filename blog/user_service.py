from typing import Dict, Any, List
from django.contrib.auth import authenticate
from blog.models import User, Post, Comment
from django.contrib.auth.models import User as DjangoUser


def get_serialized_user(uuid: str) -> Dict[str, Any]:
    user = User.objects.get(name=uuid)

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
    find_user = User.objects.get(name=user)
    find_subscriber = User.objects.get(name=subscriber)
    find_user.subscribers.add(find_subscriber)
    find_subscriber.subscribes.add(find_user)
    find_subscriber.save()
    find_user.save()
    return True


def unsubscribe(user: str, subscriber: str) -> bool:
    if user == '' or subscriber == '':
        return False
    find_user = User.objects.get(name=user)
    find_subscriber = User.objects.get(name=subscriber)
    find_subscriber.subscribes.remove(find_user)
    find_user.subscribers.remove(find_subscriber)
    find_subscriber.save()
    find_user.save()
    return True


def get_all_subscriptions(uuid: str) -> List[Dict[str, Any]]:
    user = User.objects.get(name=uuid)
    users_dict: List[Dict[str, Any]] = []
    for i in user.subscribes.all():
        users_dict.append(get_serialized_user(i.name))
    return users_dict


def delete_user(uuid: str, password: str) -> bool:
    user = User.objects.get(name=uuid)
    user.password = password
    if is_user_authenticated(user):
        django_user = authenticate(username=str(user.id), password=user.password)
        django_user.delete()
        user.delete()
        return True
    return False


def get_user(uuid: str) -> User:
    return User.objects.get(name=uuid)


def get_user_by_name(name: str) -> List[User]:
    return User.objects.filter(name__contains=name).all()


def create_user(user: User) -> bool:
    if user.is_valid():
        if user.password is not None:
            if authenticate(user.name, password=user.password) is None:
                user.save()
                django_user = DjangoUser.objects.create_user(user.name, '@', user.password)
                # чтобы проверять, одинаковые ли пользователи
                # django_user.first_name = user.id[:len(user.id)//2]
                # django_user.last_name = user.id[len(user.id)//2:]
                django_user.save()
                return True
    return False


def update_user(user: User) -> bool:
    if is_user_authenticated(user):
        django_user = authenticate(username=user.name, password=user.password)
        if django_user is not None:
            django_user.save()
            user.save()
            return True
    return False


def create_post(post: Post, author_password: str) -> bool:
    author = post.author
    author.password = author_password
    if is_user_authenticated(author):
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
            authenticated_user = authenticate(username=user.name, password=user_password)
            if authenticated_user is not None:
                return True
        if user.password is not None:
            authenticated_user = authenticate(username=user.name, password=user.password)
            if authenticated_user is not None:
                return True
    return False
