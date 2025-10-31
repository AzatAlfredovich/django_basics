from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(publication_sign=True)

    # blog/blog_list.html


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    # fields = ("heading", "content", "image", "publication_sign", "views_counter")
    success_url = reverse_lazy("blog:blogs")


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    # fields = ("heading", "content", "image", "publication_sign", "views_counter")
    success_url = reverse_lazy("blog:blogs")

    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.kwargs.get("pk")])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blogs")
