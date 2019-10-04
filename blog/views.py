from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from blog.custom_response import CustomResponse
from blog.models import User, Post, Comment
import blog.user_service as user_service
import json


@csrf_exempt
def get_user(request: HttpRequest, identity: str):
    user = user_service.get_user(identity)
    user_dict = user.to_dict()
    response = CustomResponse(user_dict)
    return HttpResponse(response.to_json())


@csrf_exempt
def get_full_user(request: HttpRequest, identity: str):
    user_dict = user_service.get_serialized_user(identity)
    response = CustomResponse(user_dict)
    return HttpResponse(response.to_json())


@csrf_exempt
def subscribe(request: HttpRequest, user, subscriber):
    is_subscribe = user_service.subscribe(request.GET['user'], request.GET['subscriber'])
    response = CustomResponse()
    response.status_from_bool(is_subscribe)
    return HttpResponse(response.to_json())


@csrf_exempt
def unsubscribe(request: HttpRequest, user, subscriber):
    is_unsubscribe = user_service.unsubscribe(request.GET['user'], request.GET['subscriber'])
    response = CustomResponse()
    response.status_from_bool(is_unsubscribe)
    return HttpResponse(response.to_json())


@csrf_exempt
def get_all_subscriptions(request: HttpRequest, identity: str):
    users_dict = user_service.get_all_subscriptions(identity)
    response = CustomResponse(users_dict)
    return HttpResponse(response.to_json())


@csrf_exempt
def delete_user(request: HttpRequest, identity: str):
    user_password_for_authentication = request.headers.get('password')
    is_deleted = user_service.delete_user(identity, user_password_for_authentication)
    response = CustomResponse()
    response.status_from_bool(is_deleted)
    return HttpResponse(response.to_json())


@csrf_exempt
def create_user(request: HttpRequest):
    user = User.from_json(request.body.decode())
    user.password = request.headers.get('password')
    is_created = user_service.create_user(user)
    response = CustomResponse()
    response.status_from_bool(is_created)
    return HttpResponse(response.to_json())


@csrf_exempt
def update_user(request: HttpRequest):
    user_from_request = User.from_json(request.body.decode())
    user_from_request.password = request.headers.get('password')
    is_updated = user_service.update_user(user_from_request)
    response = CustomResponse()
    response.status_from_bool(is_updated)
    return HttpResponse(response.to_json())


@csrf_exempt
def find_users_by_name(request, name: str):
    users = user_service.get_user_by_name(name)
    response = CustomResponse([i.to_dict() for i in users])
    return HttpResponse(response.to_json())


@csrf_exempt
def create_post(request: HttpRequest):
    post_dict = json.loads(request.body.decode())
    post = Post()
    user_password_for_authentication = request.headers.get('password')
    post.from_dict(post_dict)
    is_created = user_service.create_post(post, user_password_for_authentication)
    response = CustomResponse(response_message="User isn't authorized")
    response.status_from_bool(is_created)
    return HttpResponse(response.to_json())


@csrf_exempt
def create_comment(request: HttpRequest):
    comment = Comment()
    comment_dict: Dict[str, Any] = json.loads(request.body.decode())
    user_password_for_authentication = request.headers.get('password')
    comment.from_dict(comment_dict)
    is_created = user_service.create_comment(comment, user_password_for_authentication)
    response = CustomResponse(response_message="User isn't authorized")
    response.status_from_bool(is_created)
    return HttpResponse(response.to_json())


@csrf_exempt
def delete_comment(request: HttpRequest, identity: int):
    user_password_for_authentication = request.headers.get('password')
    is_deleted = user_service.delete_comment(identity, user_password_for_authentication)
    response = CustomResponse()
    response.status_from_bool(is_deleted)
    return HttpResponse(response.to_json())


@csrf_exempt
def delete_post(request: HttpRequest, identity: str):
    user_password_for_authentication = request.headers.get('password')
    is_deleted = user_service.delete_post(int(identity), user_password_for_authentication)
    response = CustomResponse()
    response.status_from_bool(is_deleted)
    return HttpResponse(response.to_json())
