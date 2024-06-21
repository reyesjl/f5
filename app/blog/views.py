from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ArticleForm

def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Article has been added.", extra_tags="success")
            return redirect('health-home')
    else:
        form = ArticleForm()

    return render(request, "articles/article_create.html", {"form": form})
