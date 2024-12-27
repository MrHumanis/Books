from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Shelf, Author
from django.core.paginator import Paginator
from django.views import View
from blog.forms import UserEditForm, PostForm, ShelfForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    books = Book.objects.filter(
        amount__gte=1,
    )
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def create_edit(request, book_id=None):
    book = get_object_or_404(
        Book,
        pk=book_id,
        amount__gte=1,
    )
    return render(request, 'blog/detail.html', {'post': book})


def post_detail(request, post_id):
    book = get_object_or_404(
        Book,
        pk=post_id,
    )

    if request.user != book.author:
        book = get_object_or_404(
            Book,
            pk=post_id,
            amount__gte=1,
        )
    return render(
        request,
        'blog/detail.html',
        {
            'post': book,
        }
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Shelf,
        slug=category_slug,
    )
    books = Book.objects.filter(
        amount__gte=1,
        shelf=category
    )
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/category.html',
        {
            'page_obj': page_obj,
            'category': category
        }
    )


class Profile(View):
    template = 'blog/profile.html'

    def get(self, request, **kwargs):
        name = kwargs['username']
        profile = get_object_or_404(Author, name=name)
        books = Book.objects.filter(author=profile)
        paginator = Paginator(books, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        contex = {
            "profile": profile,
            'page_obj': page_obj
        }
        return render(request, self.template, contex)


@login_required
def edit_profile(request, username):
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            user = Author.objects.get(pk=request.user.pk)
            user.name = form.cleaned_data["name"]
            user.save()
        context = {
            "form": form
        }
        return render(request, 'blog/user.html', context)
    form = UserEditForm(instance=get_object_or_404(Author, name=username))
    context = {
        "form": form
    }
    return render(request, 'blog/user.html', context)


@login_required
def post_edit(request, post_id=None):
    form = PostForm()
    if request.method == 'POST':
        if post_id is not None:
            form = PostForm(request.POST, request.FILES)
            instance = get_object_or_404(Book, pk=post_id)
            if form.is_valid():
                book = get_object_or_404(
                    Book,
                    pk=post_id
                )
                book.text = form.cleaned_data["text"]
                book.title = form.cleaned_data["title"]
                book.shelf = form.cleaned_data["shelf"]
                book.author = form.cleaned_data["author"]
                book.image = form.cleaned_data["image"]
                book.save()
                return redirect("blog:post_detail", post_id=post_id)
        else:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save()
                return redirect("blog:profile", username=book.author.name)
    else:
        if post_id is not None:
            instance = get_object_or_404(Book, pk=post_id)
            form = PostForm(instance=instance)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def post_delete(request, post_id):
    book = get_object_or_404(Book, pk=post_id)
    instance = get_object_or_404(Book, id=post_id)
    form = PostForm(instance=book)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


def create_shelf(request):
    if request.method == 'POST':
        form = ShelfForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blog:index")
    form = ShelfForm()
    context = {"form": form}
    return render(request, 'blog/create.html', context)


def create_author(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blog:index")
    form = UserEditForm()
    context = {"form": form}
    return render(request, 'blog/create.html', context)