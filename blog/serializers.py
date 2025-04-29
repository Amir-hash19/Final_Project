from rest_framework.serializers import ModelSerializer
from .models import Blog, CategoryBlog
from rest_framework import serializers




class UploadBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'slug', 'blogcategory', 'user']
        read_only_fields = ['user'] 


  




class DeleteBlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"





class ListBlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"



class BlogCategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryBlog
        fields = "__all__"