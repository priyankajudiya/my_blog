from django.contrib import messages
from django.http import HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from app_post import forms

from django.dispatch import receiver

from app_user import models
# Create your views here.

# Create Post


class createPost(CreateView):
    model = models.Post
    template_name = 'app_post/createpost.html'
    fields = ['author','title', 'image', 'text']

    def form_invalid(self, form):
        return HttpResponse('Dont try to change HTML code')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request):
        return super().dispatch(request)


# List Post

def author_list(model):
    posts = model.objects.filter(published_date__isnull=False)
    author_list = []
    for post in posts:
        if post.author.username not in author_list:
            author_list.append(post.author.username)
    return author_list


class viewPost(ListView):
    model = models.Post

    def dispatch(self, request):

        context = {
            'posts': self.model.objects.all().order_by('-published_date'),
            'author_list': author_list(self.model),
        }
        return render(request, 'app_post/allpost.html', context)

# Filter Post


def filterPost(request, author):
    model = models.Post
    fposts = model.objects.filter(author__username=author)
    posts = model.objects.all()
    if author == 'All':
        return redirect('post:viewPost')
    else:
        context = {'posts': posts,
                   'fpost': fposts,
                   'selected_author': author,
                   'author_list': author_list(model),
                   }
        return render(request, 'app_post/filteredpost.html', context)

# Detail Post


class fullPost(DetailView):
    model = models.Post
    template_name = 'app_post/fullpost.html'
    context_object_name = 'post'

# Update Post


class postUpdate(UpdateView):
    model = models.Post
    template_name = 'app_post/createpost.html'
    fields = ['title', 'image', 'text']
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponse('Not Authorized to update other post')
        return super(postUpdate, self).dispatch(request, *args, **kwargs)

# Delete Post


class postDelete(DeleteView):
    model = models.Post
    # template_name = 'app_post/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post:my_post')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.add_message(request, messages.SUCCESS, 'Post Deleted')

        if obj.author != self.request.user:
            return HttpResponse('Not authorized to delete this posts')
        return super(postDelete, self).dispatch(request, *args, **kwargs)

# User All Post


class my_post(ListView):
    model = models.Post

    def dispatch(self, request, *args, **kwargs):
        author = self.request.user
        objects = self.model.objects.filter(
            author=author).order_by('-created_date')
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return render(request, 'app_post/my_post.html', {'objects': objects})

# Not Published User All Post


def notPublishd(request):
    author = None
    if request.user.is_authenticated:
        model = models.Post
        author = request.user
        objects = model.objects.filter(
            author=author, published_date__isnull=True).order_by('-created_date')
        context = {'objects': objects,
                   'is_published': 'not',
                   }
    return render(request, 'app_post/my_post.html', context)

# Published User All Post


def Publishd(request):
    author = None
    if request.user.is_authenticated:
        model = models.Post
        author = request.user
        objects = model.objects.filter(
            author=author, published_date__isnull=False).order_by('-created_date')
        context = {'objects': objects,
                   'is_published': 'yes',
                   }
    return render(request, 'app_post/my_post.html', context)

# Publish or Drafts Post


def publish_post(request, pk, slug):
    model = models.Post
    post = model.objects.get(pk=pk)
    

    if 'next' in request.POST:
        redirect(request.POST.get('next'))

    if post.author != request.user:
        return HttpResponse('You are not authorized to Publish or Draft this post')

    if post.published_date:
        post.draft()
        return redirect('post:all_not_publish_post')
    else:
        post.publish()
        return redirect('post:all_publish_post')


# Add Comments

def addComment(request, pk):
    if request.method == 'POST':
        form = forms.commentForm(request.POST)
        form.name = request.POST.get('name')
        form.comment = request.POST.get('comment')
        form.email = request.POST.get('email')

        if form.is_valid():
            instanse = form.save(commit=False)
            instanse.post = get_object_or_404(models.Post, pk=pk)
            instanse.save()
            if request.is_ajax():
                return HttpResponse('form Saved')
        else:
            print('Not valid')
            return HttpResponse('form not Saved')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
