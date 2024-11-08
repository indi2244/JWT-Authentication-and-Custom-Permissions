from django.shortcuts import render
from .models import Item # Post
from .serializers import ItemSerializer# PostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsSuperuser, IsStaff,IsAuthenticatedOrIsSuperuser,IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class CreateUserView(APIView):
    permission_classes = [IsSuperuser]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_staff = request.data.get('is_staff', False)
        is_superuser = request.data.get('is_superuser', False)

        if not all([username, email, password]):
            return Response({"error": "Username, email, and password are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.is_staff = is_staff
            new_user.is_superuser = is_superuser
            new_user.save()
            return Response({"message": f"User '{username}' created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ItemList(APIView):# uses custom permission
    permission_classes = [IsAuthenticated,IsSuperuser] # both needs to be satisfied 

    def get(self, request):
        items=Item.objects.all()
        serializer=ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
class ItemDetail(APIView):# uses custom permission
    permission_classes = [IsAuthenticated, IsStaff] # both must be satisfied

    def get(self, request , pk):
        try:
            item=Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=ItemSerializer(item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            item= Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            item=Item.objects.get(pk=pk)
        except Item.DoesNotExist():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StaffDetail(APIView):# uses custom permission
    permission_classes = [IsSuperuser] #must be superuser to get this permission
    def get(self, request):
        staff_users = User.objects.filter(is_staff=True)
        data = [{"username": user.username, "email": user.email} for user in staff_users]
        return Response(data)


class MyProtectedView(APIView):# uses custom permission
    permission_classes = [IsAuthenticatedOrIsSuperuser]

    def get(self, request, *args, **kwargs):
        return Response({"message": "You have access to this view."})
    
class AllowanyView(APIView):
    permission_classes = [AllowAny]  # view level permissions

    def get(self, request, *args, **kwargs):
        return Response({"message": "any person who is not staff or superuser or not authenticated can also view this."})

class IsAdminView(APIView):# view level permissions
    permission_classes = [IsAdminUser]  

    def get(self, request, *args, **kwargs):
        return Response({"message": "if is_staff = True then those users can view this."})

'''class PostCreate(APIView):# uses custom permission
    permission_classes = [IsAuthenticated] # both needs to be satisfied 

    def get(self, request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):# object level permission
    permission_classes = [IsOwnerOrReadOnly]  # Apply the custom permission here

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)  #This is where the custom permission (IsOwnerOrReadOnly) is checked.

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, post)  # Check custom permission

        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)'''