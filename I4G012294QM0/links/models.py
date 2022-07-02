from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.


class Link(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
        
    )

    # DB Fields
    description = models.CharField(max_length=200)
    target_url = models.URLField(max_length = 200)
    identifier = models.SlugField(max_length=20, blank=True, unique=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )

    class Meta:
        ordering = ("-publish",)

    def save(self, *args, **kwargs):
        self.identifier = slugify(self.description)
        super().save(*args, **kwargs)
        pass 

    def __str__(self):
        return self.description
    
    def get_absolute_url(self):
        return reverse("link:post_detail", kwargs={"identifier": self.identifier})