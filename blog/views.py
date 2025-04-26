from rest_framework.generics import CreateAPIView, ListAPIView
from . models import Blog, CategoryBlog
from .serializers import UploadBlogSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from account.permissions import GroupPermission





class UploadBlogView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = UploadBlogSerializer
    permission_classes = [IsAuthenticated, GroupPermission('SupportPanel')]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
