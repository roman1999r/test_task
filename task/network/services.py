import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed

from .models import User, Like, Post
from .serializers import PostSerializer, LikeSerializer


def check_user_token(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Error')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Error')

    user = User.objects.filter(id=payload['id']).first()
    user.last_request = datetime.datetime.now()
    user.save()
    return user


def create_post(request):
    user = check_user_token(request=request)
    request.data['userId'] = user.pk
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return "Error create"


def get_filter_post(request):
    user = check_user_token(request)
    date_to = request.GET.get('date_to')
    date_from = request.GET.get('date_from')
    if not date_to:
        like = Like.objects.filter(data__gte=date_from)
    elif not date_from:
        like = Like.objects.filter(data__lte=date_to)
    else:
        like = Like.objects.filter(data__lte=date_to, data__gte=date_from)
    serializer = LikeSerializer(like, many=True)
    return serializer.data


def get_post(request, pk):
    user = check_user_token(request)
    post = Post.objects.filter(pk=pk).first()
    like = Like.objects.filter(postId=pk, like=True).count()
    print(like)
    post.likes = like
    post.save()
    serializer = PostSerializer(post)
    return serializer.data


def take_like(request):
    user = check_user_token(request)
    like = Like.objects.filter(userId=user.id, postId=request.data['postId']).first()
    if like:
        like.like = not like.like
        like.save()
        serializer = LikeSerializer(like)
        return serializer.data
    else:
        request.data['like'] = True
        request.data['userId'] = user.id
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
