import uuid

from django.test import TestCase

# Create your tests here.
from blog.user_service import *


class UserServiceTest(TestCase):

    def reset_models(self):
        self.test_user = User(
            name='maksimka',
            is_authorized=True,
            image_url='https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing',
            id=uuid.uuid4(),
            password='password'
        )

        self.second_test_user = User(
            name='kirilka',
            is_authorized=False,
            image_url='https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing',
            id=uuid.uuid4(),
        )

        self.test_post = Post(
            title="test post",
            content="test content",
            image_url='https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing',
        )

        self.test_comment = Comment(
            content='comment content',
            author_image_url='https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing'
        )

    def setUp(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        self.reset_models()

    def test_user_save(self):
        create_user(self.test_user)
        test_user_from_db = get_user(self.test_user.id)
        self.assertEquals(self.test_user, test_user_from_db, msg='users are equals')

    def test_subscribe(self):
        create_user(self.test_user)
        create_user(self.second_test_user)
        self.test_user.subscribers.add(self.second_test_user)
        self.second_test_user.subscribes.add(self.test_user)
        update_user(self.test_user)
        update_user(self.second_test_user)
        self.assertEquals(self.test_user, get_user(self.test_user.id), msg='user are equals')
        self.assertEquals(self.test_user.subscribes, get_user(self.test_user.id).subscribes,
                          msg='subscribes are equals')
        self.assertEquals(self.test_user.subscribers, get_user(self.test_user.id).subscribers,
                          msg='subscribers are equals')

    def test_post_save(self):
        self.test_post.author = self.test_user
        create_user(self.test_user)
        create_post(self.test_post, self.test_user.password)
        self.test_user.post_set.add(self.test_post)
        update_user(self.test_user)
        self.assertEquals(self.test_user, get_user(self.test_user.id), msg='users are equals')
        self.assertEquals(self.test_post, get_post(self.test_post.id), msg='posts are equals')
        self.assertEquals(self.test_user.post_set, get_user(self.test_user.id).post_set, msg='user posts are equals')
        create_user(self.second_test_user)
        self.test_post.author = self.second_test_user
        self.assertFalse(create_post(self.test_post, self.test_user.password), msg='create user')

    def test_comment_save(self):
        self.assertTrue(create_user(self.test_user))
        self.test_post.author = self.test_user
        self.assertTrue(create_post(self.test_post, self.test_user.password))
        self.test_comment.author = self.test_user
        self.test_comment.post = self.test_post
        create_comment(self.test_comment, self.test_user.password)
        self.assertEquals(self.test_comment, get_comment(self.test_comment.id), msg='comments are equals')
        self.assertEquals(self.test_post.comment_set, get_post(self.test_post.id).comment_set,
                          msg='comments in posts are equals')

    def test_user_serializing(self):
        deserialized_user = User()
        deserialized_user.from_dict(self.test_user.to_dict())
        self.assertEquals(self.test_user, deserialized_user)

    def test_post_serializing(self):
        self.test_post.author = self.test_user
        create_user(self.test_user)
        create_post(self.test_post, self.test_user.password)
        deserialized_post = Post()
        deserialized_post.from_dict(self.test_post.to_dict())
        print(deserialized_post)
        self.assertEquals(self.test_post, deserialized_post)

    def test_comment_serializing(self):
        self.test_post.author = self.test_user
        create_user(self.test_user)
        create_post(self.test_post, self.test_user.password)
        create_comment(self.test_comment, self.test_user.password)
        self.test_comment.author = self.test_user
        self.test_comment.post = self.test_post
        deserialized_comment = Comment()
        deserialized_comment.from_dict(self.test_comment.to_dict())
        self.assertEquals(self.test_comment, deserialized_comment)
