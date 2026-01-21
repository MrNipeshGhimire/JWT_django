from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer

@api_view(['POST','GET'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        print(username,email,password)
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()
            return Response({'msg':"User registered successfully"},status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e)


# for token
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh),
        'access' :  str(refresh.access_token)
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error':"Username and password is required"},status=status.HTTP_400_BAD_REQUEST)
        
        # for checking valid user or not 
        user = authenticate(username=username, password=password)

        if user is not None:
           token = get_token_for_user(user)
           serializer = UserSerializer(user)
           return Response({'msg':"User logged in successfully",'token':token, 'user':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'error':"Invalid credintial"},status=status.HTTP_401_UNAUTHORIZED)
        
        
        





    
