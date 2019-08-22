from typing import List
from blog.models import Post, User, Comment


def get_user_posts(user: User) -> List[Post]:
    posts = Post.objects.filter(author=user)
    return posts
