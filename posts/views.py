# Note: ListView is used to get all the post records
#       while DetailView is used to get just one record
#       from the database.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post
from .forms import PostCreateForm, PostUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from taggit.models import Tag


# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


@method_decorator(login_required(login_url='/registration/login'), name='dispatch')
class CreatePostView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'create_post.html'

    # Save logged-in user as post author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


@method_decorator(login_required(login_url='/registration/login'), name='dispatch')
class UpdatePostView(UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'update_post.html'


# uid is post user id
# pk is post primary key
def delete_post(request, uid, pk):
    # check if post author id matches logged-in users id
    if uid == request.user.id:
        post = Post.objects.get(pk=pk)
        post.delete()
    return redirect('home')


def tags_view(request, tag):
    # Filter tags from the tag parameter passed from url
    tags = Tag.objects.filter(slug=tag).values_list('name', flat=True)
    # Filter posts based on tags
    posts = Post.objects.filter(tags__name__in=tags)

    return render(request, 'tag_posts.html', {'tag': tag, 'posts': posts})
