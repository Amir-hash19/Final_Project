from django.urls import path
from .views import UploadBlogView


urlpatterns = [
    path("upload-blog/", UploadBlogView.as_view(), name="uploadblog"),
]
