import json
from typing import Dict, Any, NoReturn
from django.core import serializers
from django.db.models import *


class User(Model):

    name = CharField(max_length=30, primary_key=True)

    image_url = URLField(max_length=100)

    subscribers = ManyToManyField('self', related_name='subscribers+', blank=True, symmetrical=False)

    subscribes = ManyToManyField('self', related_name='subscribes+', blank=True, symmetrical=False)

    password: str

    USERNAME_FIELD = 'name'

    def is_valid(self) -> bool:
        if self.name is not None:
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        user_dict: Dict[str, Any] = serializers.serialize('python', [self])[0]['fields']
        user_dict['posts'] = []
        user_dict['name'] = self.name
        return dict(user_dict)

    def from_dict(self, user: Dict[str, Any]) -> NoReturn:
        for key, value in user.items():
            if key == 'subscribers':
                self.subscribers.set(value)

            elif key == 'password':
                self.password = value

            elif key == 'subscribes':
                self.subscribes.set(value)

            elif hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def from_json(cls, json_user: str) -> 'User':
        if json_user is not None and json_user != '':
            user_dict: Dict[str, Any] = json.loads(json_user)
            user = User()
            user.from_dict(user_dict)
            return user
        else:
            return User()

    def __str__(self):
        return 'name: {0}'.format(self.name)


class Post(Model):

    author = ForeignKey(User, on_delete=CASCADE, serialize=False)

    title = CharField(max_length=100)

    content = TextField(default='')

    image_url = URLField(max_length=100)

    create_date = DateField(auto_now_add=True)

    def to_dict(self) -> Dict[str, Any]:
        post_dict: Dict[str, Any] = dict(serializers.serialize('python', [self])[0]['fields'])
        post_dict['create_date'] = str(self.create_date)
        post_dict['author'] = self.author.name
        post_dict['id'] = self.id
        post_dict['comments'] = []
        return post_dict

    def from_dict(self, post: Dict[str, Any]) -> NoReturn:
        for key, value in post.items():
            if key == 'author':
                from blog.user_service import get_user
                self.author = get_user(value)
            elif hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return 'id: {0}, uuid: {1}, title: {2}'.format(self.id, self.author, self.title)


class Comment(Model):

    author = ForeignKey(User, on_delete=CASCADE, serialize=False)

    post = ForeignKey(Post, on_delete=CASCADE, default='')

    author_image_url = URLField(max_length=100)

    content = TextField(default='')

    def to_dict(self) -> Dict[str, Any]:
        comment_dict: Dict[str, Any] = serializers.serialize('python', [self])[0]['fields']
        comment_dict['id'] = self.id
        comment_dict['post'] = self.post.id
        comment_dict['author'] = self.author.id
        return comment_dict

    def from_dict(self, comment: Dict[str, Any]) -> NoReturn:
        for key, value in comment.items():
            if key == 'author':
                from blog.user_service import get_user
                self.author = get_user(value)
            elif key == 'post':
                from blog.user_service import get_post
                self.post = get_post(int(value))
            elif hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return 'id: {0}, author: {1}, content: {2}'.format(self.id, self.author, self.content)
