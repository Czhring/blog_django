from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from ..serializers.user import UserSerializer
from django.contrib.auth import authenticate, login

class SignUp(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):
        # Create the user using the UserSerializer 
        created_user = UserSerializer(data=request.data['user'])
        # Check user is valid
        if created_user.is_valid():
            # Save the user and send back a response!
            created_user.save()
            return Response({ 'user': created_user.data }, status=status.HTTP_201_CREATED)
        else:
            return Response(created_user.errors, status=status.HTTP_400_BAD_REQUEST)

class SignIn(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        data = request.data['user']
        # use django authenticate to verify password and email match
        user = authenticate(request, email=data['email'], password=data['password'])
        # Is our user is successfully authenticated...
        if user is not None:  
            login(request, user)
            # use django generate a token and save it to user
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            user.token = token.key
            user.save()
            # return the user with their id, email and token
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'token': token.key
                }
            })
        else:
            return Response({ 'msg': 'The username and/or password is incorrect.' }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)