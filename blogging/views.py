from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from rest_framework import viewsets, permissions
from blogging.models import Post, Category
from blogging.forms import MyPostForm
from blogging.serializers import UserSerializer, PostSerializer, CategorySerializer


def add_model(request):

    if request.method == "POST":
        form = MyPostForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.published_date = timezone.now()
            model_instance.save()
            return redirect("/")
    else:
        form = MyPostForm()
        return render(request, "blogging/add.html", {"form": form})


class PostListView(ListView):
    queryset = Post.objects.exclude(published_date__exact=None).order_by(
        "-published_date"
    )
    template_name = "blogging/list.html"


class PostDetailView(DetailView):
    queryset = Post.objects.exclude(published_date__exact=None)
    template_name = "blogging/detail.html"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.exclude(published_date__exact=None).order_by(
        "-published_date"
    )
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LatestPostsFeed(Feed):
    title = "Cool Posts"
    link = "/feed/"
    description = "Cool posts from the mind of an author"

    def items(self):
        return Post.objects.exclude(published_date__exact=None).order_by(
            "-published_date"
        )[:5]

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return post.text

    def item_link(self, post):
        return reverse("blog_detail", args=[post.pk])


# def stub_view(request, *args, **kwargs):
#     body = "Stub View\n\n"
#     if args:
#         body += "Args:\n"
#         body += "\n".join(["\t%s" % a for a in args])
#     if kwargs:
#         body += "Kwargs:\n"
#         body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
#     return HttpResponse(body, content_type="text/plain")

# def list_view(request):
#     published = Post.objects.exclude(published_date__exact=None)
#     posts = published.order_by('-published_date')
#     template = loader.get_template('blogging/list.html')
#     context = {'posts': posts}
#     body = template.render(context)
#     return HttpResponse(body, content_type="text/html")


# def list_view(request):
#     published = Post.objects.exclude(published_date__exact=None)
#     posts = published.order_by('-published_date')
#     context = {'posts': posts}
#     return render(request, 'blogging/list.html', context)

# def detail_view(request, post_id):
#     published = Post.objects.exclude(published_date__exact=None)
#     try:
#         post = published.get(pk=post_id)
#     except Post.DoesNotExist:
#         raise Http404
#     context = {'post': post}
#     return render(request, 'blogging/detail.html', context)
