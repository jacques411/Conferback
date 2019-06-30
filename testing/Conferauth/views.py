from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

from .serializer import CuserSeri
from .models import Cuser

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes, parser_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

def profile_view(request, username):
    u = Cuser.objects.get(username=username)
    s = CuserSeri(instance=u, context={'request':request})
    print (s.data)
    return Response(s.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)

@api_view(['POST'])
@csrf_exempt
def login(request):
    user=authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is not None:
        auth_login(request,user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'user not found'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@csrf_exempt
def logout(request):
    user=request.user
    if user is not None:
        user.auth_token.delete()
        return Response({'logout': 'Token for user ' + user.username + ' deleted'}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'user not found'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@csrf_exempt
def create_user(request):
        print (type(request))
        u = Cuser(username=request.data.get('username'),
        	first_name=request.data['first_name'],last_name=request.data['last_name']
        	,email=request.data['email'])
        print
        u.set_password(request.data['password'])
        u.save()
        s = CuserSeri(instance=u, context={'request':request})
        print (s.data)
        return Response(s.data,status=status.HTTP_200_OK)

class CuserView(viewsets.ModelViewSet):
    queryset = Cuser.objects.all()
    serializer_class = CuserSeri
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, pk=None):
        u = Cuser.objects.get(username=request.data.get('username'))
        u.delete()
        return Response({"succes": "user : " + u.username + " deleted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def other(self, request, pk=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth), # None
            'other': str(request.user)
            }
        return Response(content)
