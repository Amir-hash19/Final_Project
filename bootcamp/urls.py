from django.urls import path
from .views import (CreateBootCampCategoryView, CreateBootCampView, DeleteBootCampCategoryView, DeleteBootCampView, 
ListBootcampView, ListBootCampCategoryView, UpdateBootCampView, ListAvailableBootCamp, CreateRegisterBootCampView, ListRegisterBootCampView, EditRegisterBootCampView)



urlpatterns = [
    path("add-category-bootcamp/", CreateBootCampCategoryView.as_view(), name="add-category-bootcamp"),
    path("add-bootcamp/", CreateBootCampView.as_view(), name="add-bootcamp"),
    path("delete-bootcamp-category/<int:pk>", DeleteBootCampCategoryView.as_view(), name="delete-bootcamp-category"),
    path("delete-bootcamp/<int:pk>", DeleteBootCampView.as_view(), name="delete-bootcamp"),
    path("list-bootcamps/", ListBootcampView.as_view(), name="bootcamp-list"),
    path("list-bootcamp-category/", ListBootCampCategoryView.as_view(), name="list-bootcamp-category"),
    path("edit-bootcamp/<int:pk>", UpdateBootCampView.as_view(), name="edit-bootcamp"),
    path("available-bootcamp/", ListAvailableBootCamp.as_view(), name="available-bootcams"),
    path("register-bootcamp/", CreateRegisterBootCampView.as_view(), name="register-bootcamp"),
    path("list-register-bootcamp/", ListRegisterBootCampView.as_view(), name="list-register-bootcamp"),
    path("review-bootcamp-register/<int:pk>", EditRegisterBootCampView.as_view(), name="review-register-bootcamp"),
]