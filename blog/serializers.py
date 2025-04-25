from rest_framework.serializers import ModelSerializer
from .models import Blog, CategoryBlog
from rest_framework import serializers




class UploadBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'slug', 'blogcategory', 'user']
        read_only_fields = ['user']  # کاربر نتونه خودش مقدار بده

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # فقط کاربر لاگین‌شده
        return super().create(validated_data)
