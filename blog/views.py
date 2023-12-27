from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import PostForm, TagForm
from .models import Post, Tag
from .utils import (ObjectCreateMixin, ObjectDeleteMixin, ObjectDetailMixin,
                    ObjectUpdateMixin)


def posts_list(request):
    tags = Tag.objects.all()
    last_post = Post.objects.latest('date_pub')
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.published().order_by("-date_pub")[1:]

    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    context = {
        'tags': tags,
        'last_object': last_post,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixin, DetailView):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, CreateView):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, UpdateView):
    model = Post
    fields = '__all__'
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, DeleteView):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, DetailView):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, CreateView):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, UpdateView):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, DeleteView):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


class StartHereView(View):
    template_name = 'blog/start_here.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
