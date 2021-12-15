from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from ..serializers.blog import BlogSerializer
from ..models.blog import Blog

class BlogsView(APIView):
    def post(self, request):
        # Add the user id as owner
        request.data['owner'] = request.user.id
        blog = BlogSerializer(data=request.data)
        if blog.is_valid():
            blog.save()
            return Response(blog.data, status=status.HTTP_201_CREATED)
        else:
            return Response(blog.errors, status=status.HTTP_400_BAD_REQUEST)  

    def get(self, request):
        # filter for Blogs with our user id
        blogs = Blog.objects.filter(owner=request.user.id)
        data = BlogSerializer(blogs, many=True).data
        return Response(data)


class BlogView(APIView):
    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        # Check the Blog's owner against the user making this request
        if request.user != blog.owner:
            raise PermissionDenied('Unauthorized, you do not own this Blog')
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if request.user != blog.owner:
            raise PermissionDenied('Unauthorized, you do not own this Blog')
        data = BlogSerializer(blog).data
        return Response(data)
    
    def patch(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        # Check the Blog's owner against the user making this request
        if request.user != blog.owner:
            raise PermissionDenied('Unauthorized, you do not own this Blog')
        # Ensure the owner field is set to the current user's ID
        request.data['owner'] = request.user.id
        updated_blog = BlogSerializer(Blog, data=request.data)
        if updated_blog.is_valid():
            updated_blog.save()
            return Response(updated_blog.data)
        return Response(updated_blog.errors, status=status.HTTP_400_BAD_REQUEST)