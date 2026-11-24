from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.book_list),
    path('books/<int:book_pk>/', views.book_detail),
    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('books/<int:book_pk>/comments/', views.comment_create),
]
