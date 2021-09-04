from django.conf.urls import url
from django.urls import path, include, re_path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.MoviesView.as_view(), name="movie_list"),
    path('order_by=<order>', views.MoviesView.as_view(), name="sort_movies"),
    path('<int:user_id>/', views.UserMoviesView.as_view(), name="user_movies"),
    path('<int:user_id>/order_by=<order>', views.UserMoviesView.as_view(), name="sort_user_movies"),
    path('react/', views.react_to_movie, name="react_to_movie"),
    path('add/', views.add_movie, name="add_movie"),

]
