from django.urls import path #to be able to add path

from . import  views #to ensure that we are able to access views.py
 
urlpatterns = [
    path("",views.index),
    #path("<int:id>", views.book_detail, name = "book-detail"), #<> indicates a dynamic segment here, there is the same id that was defined in views
    path("<slug:slug>", views.book_detail_slug, name = "book-detail-slug")
]
