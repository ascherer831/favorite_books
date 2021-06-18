from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('user/create', views.register),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('books', views.success),
    path('books/create', views.create),
    path('books/<int:book_id>', views.info),
    path('books/<int:book_id>/update', views.update),
    path('books/<int:book_id>/favorite', views.favorite),
    path('books/<int:book_id>/favorite_main', views.favorite_main),
    path('books/<int:book_id>/unfavorite', views.unfavorite),
]