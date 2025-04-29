from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from . models import Blog, CategoryBlog
from .serializers import UploadBlogSerializer, DeleteBlogSerializer, ListBlogSerializer, BlogCategorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from account.permissions import GroupPermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



class CustomPagination(PageNumberPagination):
    page_size = 40



class UploadBlogView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = UploadBlogSerializer
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]

    def perform_create(self, serializer):
        serializer.save(
            user = self.request.user
        )





#اضافه کردن دسته بندی توسط سوپریوزر و پنل ادمین
class AddCategoryBlogView(CreateAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    serializer_class = BlogCategorySerializer





class DeleteBlogView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = DeleteBlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)
        






class DeleteCategoryBlogView(DestroyAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BlogCategorySerializer








#دیدن لیست مقالات برای کابر عادی
class ListBlogView(ListAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ListBlogSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    filterset_fields = ["blogcategory", "user"]
    ordering_fields = ["uploaded_at"]







#دیدن جزییات مقاله توسظ کاربر عادی
class DetailBlogView(RetrieveAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ListBlogSerializer






#بروزرسانی مقالات توسط تیم پنل و سوپریوزر
class UpdateBlogView(UpdateAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]
    serializer_class = ListBlogSerializer





class EditBlogView(UpdateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel")]
    serializer_class = ListBlogSerializer


    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)




