from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(visibility="published")

    def drafts(self):
        return self.filter(visibility="draft")

    def featured(self):
        return self.filter(featured=True)

    def by_slug(self, slug):
        return self.get(slug=slug)

    def by_visibility(self, visibility):
        return self.filter(visibility=visibility)

    def by_tag(self, tag):
        return self.filter(tags__icontains=tag)

    def by_type(self, type):
        return self.filter(type=type)

class Article(models.Model):
    VISIBILITY_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    TYPE_CHOICES = (
        ("strength_and_conditioning", "Strength & Conditioning"),
        ("nutrition", "Nutrition"),
        ("mental", "Mental"),
        ("other", "Other"),
    )

    READING_TIME_CHOICES = (
        (5, "5 mins"),
        (10, "10 mins"),
        (15, "15 mins"),
        (20, "20 mins"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.CharField(max_length=50, blank=True)
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default="other"
    )
    featured = models.BooleanField(default=False)
    excerpt = models.TextField(max_length=300, blank=True)
    content = CKEditor5Field(
        "Text", config_name="extends", default=None, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="draft")
    reading_time = models.IntegerField(choices=READING_TIME_CHOICES, default=5)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.created_at:
                self.created_at = timezone.now()
            date_str = self.created_at.strftime("%Y-%m-%d")
            self.slug = slugify(f"{self.title}-{date_str}")
        super().save(*args, **kwargs)

    def add_view(self):
        self.views += 1
        self.save(update_fields=["views"])

    def __str__(self):
        return self.title
