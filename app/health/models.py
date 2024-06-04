from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')

    def drafts(self):
        return self.filter(status='draft')
    
    def featured(self):
        return self.filter(featured=True)
    
    def by_slug(self, slug):
        return self.get(slug=slug)
    
    def by_visibility(self, visibility):
        if visibility == 'published':
            return self.filter(status='published')
        elif visibility == 'draft':
            return self.filter(status='draft')
        return self
    
    def by_tag(self, tag):
        return self.filter(tags__icontains=tag)
    
class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def drafts(self):
        return self.get_queryset().drafts()
    
    def featured(self):
        return self.get_queryset().featured()
    
    def by_slug(self, slug):
        return self.get_queryset().by_slug(slug)
    
    def by_visibility(self, visibility):
        return self.get_queryset().by_visibility(visibility)
    
    def by_tag(self, tag):
        return self.get_queryset().by_tag(tag)
    

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    author = models.CharField(max_length=50, blank=True)
    featured = models.BooleanField(default=False)
    excerpt = models.TextField(max_length=300, blank=True)
    content = CKEditor5Field('Text', config_name='extends', default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, blank=True)
    featured_image = models.ImageField(upload_to='featured_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    reading_time = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.created_at:
                self.created_at = timezone.now()
            date_str = self.created_at.strftime("%Y-%m-%d")
            self.slug = slugify(f"{self.title}-{date_str}")
        super().save(*args, **kwargs)

    def add_view(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title
