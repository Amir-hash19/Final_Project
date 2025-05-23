from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("login-signup/", include("account.urls")),
    path("blogs/", include("blog.urls")),
    path("bootcamps/", include("bootcamp.urls")),
    path("feedbacks/", include("support.urls")),
]
