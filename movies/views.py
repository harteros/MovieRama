from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Movie


class MoviesView(generic.ListView):
    """
        Displays the list of movies

        **Context**

            ``movies``
                The list of movies

        **Template:**

            :template:`movies/index.html`
    """
    model = Movie
    template_name = "movies/index.html"
    context_object_name = "movies"

    def get_ordering(self):
        """
            Displays the list of movies based on the defined argument
        """
        if 'order' in self.kwargs:
            if self.kwargs['order'] == 'pub_date':
                ordering = "-" + self.kwargs['order']
            else:
                ordering = self.kwargs['order']
            return ordering
        else:
            return '-pub_date'


class UserMoviesView(MoviesView):
    """
        Displays the list of the user's movies

        **Context**

            ``movies``
                The list of user's movies

        **Template:**

            :template:`movies/index.html`
    """

    def get_queryset(self):
        """
            Returns the movies posted by the user with the specified user_id
        """
        queryset = super(MoviesView, self).get_queryset()
        queryset = queryset.filter(user_id=self.kwargs['user_id'])
        return queryset

    def get_context_data(self, **kwargs):
        """
            Passes the user_id to the context to be usable in the template
        """
        context = super(MoviesView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        return context


@login_required(login_url='/accounts/login/')
def react_to_movie(request):
    """
        Updates the list of likes or hates of the movie based on the user's selection.
        The user should be logged in order to be able to react to a movie.
    """
    if request.method == "POST":
        movie_id = request.POST.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        if 'like_btn' in request.POST:
            if request.user in movie.likes.all():
                movie.likes.remove(request.user)
            else:
                movie.likes.add(request.user)
                movie.hates.remove(request.user)
        elif 'hate_btn' in request.POST:
            if request.user in movie.hates.all():
                movie.hates.remove(request.user)
            else:
                movie.hates.add(request.user)
                movie.likes.remove(request.user)
        return HttpResponseRedirect(reverse('movies:movie_list'))


@login_required(login_url='/accounts/login/')
def add_movie(request):
    """
        Display a form to create a new :model:`movies.Movie`.

        **Template:**

            :template:`movies/add.html`
    """
    if request.method == "POST":
        movie_title = request.POST.get('title')
        movie_desc = request.POST.get('desc')
        movie = Movie(title=movie_title, desc=movie_desc, pub_date=datetime.now(), user=request.user)
        movie.save()
        return HttpResponseRedirect(reverse('movies:movie_list'))
    return render(request, 'movies/add.html')
