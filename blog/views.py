from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from . models import Blog, CategoryBlog
from .serializers import UploadBlogSerializer, DeleteBlogSerializer, ListBlogSerializer, BlogCategorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from account.permissions import GroupPermission





class UploadBlogView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = UploadBlogSerializer
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context





#اضافه کردن دسته بندی توسط سوپریوزر و پنل ادمین
class AddCategoryBlogView(CreateAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]





class DeleteBlogView(DestroyAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = DeleteBlogSerializer






class DeleteCategoryBlogView(DestroyAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BlogCategorySerializer








#دیدن لیست مقالات برای کابر عادی
class ListBlogView(ListAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ListBlogSerializer






#دیدن جزییات مقاله توسظ کاربر عادی
class DetailBlogView(RetrieveAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ListBlogSerializer







class UpdateBlogView(UpdateAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = ListBlogSerializer








