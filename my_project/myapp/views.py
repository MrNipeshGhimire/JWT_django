from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer,BlogSerializer
from .models import Blog

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
        
        
        
# for inserting blog
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def blog_view(request):
    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"msg":"Blog added successfully","blog":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"Unable to add blog","err":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        blog = Blog.objects.all()
        serializer = BlogSerializer(blog, many=True)
        return Response(serializer.data)



@api_view(['PUT','DELETE','GET'])
def blog_view_detail(request,id):
    try:
        blog = Blog.objects.get(id=id)  # select * from Blog where id=id 
    
    except Exception as e:
        print(e)
        return Response({"error":"Cannot find blog"})
    
    if request.method == 'DELETE':
        if blog.author == request.user:
            blog.delete()
            return Response({'msg':"Blog deleted successfully !! "})
        else:
            return Response({"error":"You are not authorized to delete this blog"})
        
    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        if blog.author == request.user:
            serializer = BlogSerializer(blog,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':"Blog updated successfully",'updated_blog':serializer.data})
            else:
                return Response({'eror':serializer.errors})
        else:
            return Response({'error':"You are not authorized to edit this blog"},status=status.HTTP_401_UNAUTHORIZED)


