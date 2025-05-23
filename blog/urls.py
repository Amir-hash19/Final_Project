from django.urls import path
from .views import (UploadBlogView, DeleteBlogView, ListBlogView, UpdateBlogView, AddCategoryBlogView, 
                    DeleteCategoryBlogView, EditBlogView, DownLoadBlog)


urlpatterns = [
    path("upload-blog/", UploadBlogView.as_view(), name="upload-blog"),
    path("delete-blog/<int:pk>", DeleteBlogView.as_view(), name="delete-blog"),
    path("blogs-list", ListBlogView.as_view(), name="blogs-list"),
    path("update-blog/<int:pk>", UpdateBlogView.as_view(), name="update-blog"),
    path("add-category-blog/", AddCategoryBlogView.as_view(), name="create-category-blog"),
    path("delete-category-blog/<int:pk>", DeleteCategoryBlogView.as_view(), name="delete-category-blog"),
    path("edit-blog-only-admin/", EditBlogView.as_view(), name="edit-blog-only-admin"),
    path("blog/<int:pk>/download/", DownLoadBlog.as_view(), name="download-blog"),
]
