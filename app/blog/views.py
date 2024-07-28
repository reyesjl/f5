from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ArticleForm
from core.utils import check_user, get_object_or_error
from core.decorator import user_has_role, is_staff, is_trainer, is_staff_or_trainer
from .models import Article

def index(request):
    articles = Article.objects.published()

    context = {
        "articles": articles,
    }

    return render(request, "articles/index.html", context)

@is_staff_or_trainer
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.username
            article.save()
            messages.success(request, "Article has been added.", extra_tags="success")
            return redirect('health-home')
    else:
        form = ArticleForm()

    return render(request, "articles/article_form.html", {"form": form})

def article_detail(request, slug):
    article = get_object_or_error(Article, slug=slug)
    
    context = {
        "article": article,
    }

    return render(request, "articles/article_detail.html", context)

@is_staff_or_trainer
def article_update(request, slug):
    article = get_object_or_error(Article, slug=slug)
    
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.username
            article.save()
            messages.success(request, "Article has been updated.", extra_tags="success")
            return redirect('article-detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, "articles/article_form.html", {"form": form})

@is_staff_or_trainer
def article_delete(request, slug):
    article = get_object_or_error(Article, slug=slug)
    
    if request.method == "POST":
        article.delete()
        messages.success(request, f"Article has been deleted.", extra_tags="success")
        return redirect("health-home")
    
    return render(request, "articles/article_delete_confirm.html", {"article": article})