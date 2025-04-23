from django.db import models
from account.models import CustomUser



class CategoryBlog(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name



class Blog(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=100)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    blogcategory = models.ForeignKey(to=CategoryBlog, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.title} - {self.status}"



