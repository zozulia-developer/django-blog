from django.db import models
from django.shortcuts import reverse
from django.conf import settings

from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class PostManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(status=Post.PUBLISHED)

    def drafted(self):
        return self.get_queryset().filter(status=Post.DRAFT)

    def archived(self):
        return self.get_queryset().filter(status=Post.ARCHIVED)


class Post(models.Model):
    DRAFT = 1
    PUBLISHED = 2
    ARCHIVED = 3
    DEFAULT_IMG = 'default/default.png'

    objects = PostManager()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True)
    title = models.CharField(
        _('Article Title'),
        max_length=150,
        db_index=True)
    slug = models.SlugField(
        _('Slug'),
        max_length=150,
        blank=True,
        unique=True)
    body = models.TextField(
        blank=True,
        db_index=True)
    status = models.PositiveSmallIntegerField(
        _('Status'),
        db_index=True,
        choices=(
            (DRAFT, _('Draft')),
            (PUBLISHED, _('Published')),
            (ARCHIVED, _('Archived'))
        ), default=DRAFT)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/blog/%Y/%m/%d',
        help_text='150x150px',
        verbose_name='Image link',
        default=DEFAULT_IMG)
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='posts')
    date_pub = models.DateTimeField(
        _('Created At'),
        auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def image_img(self):
        if self.image:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"></a>'.format(self.image.url))
        else:
            return '(No image)'

    image_img.short_description = 'Image'
    image_img.allow_tags = True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

        indexes = [
            models.Index(fields=['author', 'status'], name='author_status_idx')
        ]
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
