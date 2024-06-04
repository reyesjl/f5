from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Post
from .forms import PostForm
from core.utils import check_user
from core.decorator import user_has_role


def index(request):
    posts = Post.objects.published()
    return render(request, "health/index.html", {"posts": posts})

def post_list(request):
    posts = Post.objects.published()
    can_manage = check_user(request.user, "health_manager")

    # Filter on post visibility
    post_visibility = request.GET.get("post_visibility")
    if post_visibility and can_manage:
        posts = Post.objects.all()
        posts = posts.by_visibility(post_visibility)

    # Filter on post status    
    post_status = request.GET.get("post_status")
    if post_status == "featured":
        posts = posts.featured()

    # Filter on post focus (tags)
    post_focus = request.GET.get("post_focus")
    if post_focus:
        if post_focus != 'all':
            posts = posts.by_tag(post_focus)

    context = {
        "posts": posts,
        "can_manage": can_manage,
    }
    return render(request, "posts/post_list.html", context)

@user_has_role("health_manager")
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("post-list"))
    else:
        form = PostForm()

    return render(request, "posts/post_create.html", {"form": form})

def post_detail(request, post_slug):
    try:
        post = Post.objects.by_slug(slug=post_slug)
    except Exception as e:
        message = e
        return render(request, "posts/post_error.html", {"message": message})

    # update post views
    post_id = post.id
    viewed_posts = request.session.get("viewed_posts", [])
    if post_id not in viewed_posts:
        # Update post views and add post ID to viewed_posts
        post.add_view()
        viewed_posts.append(post_id)  # Convert to list
        request.session["viewed_posts"] = viewed_posts
    else: 
        print(viewed_posts)

    can_manage = check_user(request.user, "health_manager")

    context = {
        "post": post,
        "can_manage": can_manage,
    }
    return render(request, "posts/post_detail.html", context)

@user_has_role("health_manager")
def post_update(request, post_slug):
    try:
        post = Post.objects.by_slug(slug=post_slug)
    except Exception as e:
        message = e
        return render(request, "posts/post_error.html", {"message": message})
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse("post-list"))
    else:
        form = PostForm(instance=post)

    return render(request, "posts/post_update.html", {"form": form})

@user_has_role("health_manager")
def post_delete(request, post_slug):
    try:
        post = Post.objects.by_slug(slug=post_slug)
    except Exception as e:
        message = e
        return render(request, "posts/post_error.html", {"message": message})
    
    if request.method == "POST":
        post.delete()
        return redirect("post-list")
    
    return render(request, "posts/post_delete_confirm.html", {"post": post})
