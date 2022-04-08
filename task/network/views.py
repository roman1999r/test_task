import datetime
import jwt
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .models import User
from .serializers import UserSerializer


@api_view(['GET'])
def post_filter(request):
    if request.method == "GET":
        post = services.get_filter_post(request=request)
        return Response(post)


@api_view(['GET'])
def get_post_view(request, pk):
    if request.method == "GET":
        post = services.get_post(request=request, pk=pk)
        return Response(post)


@api_view(['POST'])
def take_like_view(request):
    if request.method == "POST":
        like = services.take_like(request=request)
        return Response(like)


@api_view(['POST'])
def create_post_view(request):
    if request.method == "POST":
        post = services.create_post(request=request)
        return Response(post)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed("Password")

        payload = {
            'id': user.pk,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):

    def get(self, request):
        user = services.check_user_token(request=request)
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        user = services.check_user_token(request=request)

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
