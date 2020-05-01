from django.db import models
from django.urls import reverse

from account.models import CustomUser
from account.utils import custom_slugify


class Image(models.Model):
    user = models.ForeignKey(CustomUser,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    users_like = models.ManyToManyField(CustomUser,
                                        related_name='images_likes',
                                        blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            blank=True,
                            null=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d',
                              blank=True,
                              null=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = custom_slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:image_details', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('images:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('images:delete', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    image = models.ForeignKey(Image,
                              on_delete=models.CASCADE,
                              related_name='comments')  # image.comments.all()
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='comments')  # user.comments.all()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.image}'
