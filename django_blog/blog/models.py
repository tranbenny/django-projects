from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# custom Post Manager class
# Model Managers allow you to filter on specific values in a queryset
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')



class Post(models.Model):
    objects = models.Manager() # default manager
    published = PublishedManager() # custom manager

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    # slug = used in URLs, short lbel with only letters, numbers, underscores, hyphens
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # meta data
    # tells django to sort results based on publish field in descending order
    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    # build a canonical URL for Post objects
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
