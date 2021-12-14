from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers.user import UserSerializer

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