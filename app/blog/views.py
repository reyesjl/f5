from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ArticleForm
from core.utils import check_user, get_object_or_error
from core.decorator import user_has_role
from .models import Article

def index(request):
    articles = Article.objects.published()
    can_manage = check_user(request.user, "blog_manager")

    context = {
        "articles": articles,
        "can_manage": can_manage,
    }

    return render(request, "articles/index.html", context)

@user_has_role("blog_manager")
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
    can_manage = check_user(request.user, "blog_manager")
    try:
        article = Article.objects.by_slug(slug=slug)
    except Article.DoesNotExist:
        messages.error(request, f"The requested article does not exists.", extra_tags="error")
    except Exception as e:
        messages.error(request, f"An unexpected error occured: {e}", extra_tags="error")
        return render(request, "core/error.html")
    
    if not can_manage and article.visibility == 'draft':
        messages.error(request, f"This article is not published.", extra_tags="error")
        return render(request, "core/error.html")
    
    context = {
        "article": article,
        "can_manage": can_manage
    }

    return render(request, "articles/article_detail.html", context)

@user_has_role("blog_manager")
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

@user_has_role("blog_manager")
def article_delete(request, slug):
    try:
        article = Article.objects.by_slug(slug=slug)
    except Article.DoesNotExist:
        messages.error(request, f"The requested article does not exists.", extra_tags="error")
    except Exception as e:
        messages.error(request, f"An unexpected error occured: {e}", extra_tags="error")
        return render(request, "core/error.html")
    
    if request.method == "POST":
        article.delete()
        messages.success(request, f"Article has been deleted.", extra_tags="success")
        return redirect("health-home")
    
    return render(request, "articles/article_delete_confirm.html", {"article": article})