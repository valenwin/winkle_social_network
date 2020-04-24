from django.db import models
from account.models import CustomUser
from account.utils import custom_slugify


class Image(models.Model):
    user = models.ForeignKey(CustomUser, related_name='images_created', on_delete=models.CASCADE)
    users_like = models.ManyToManyField(CustomUser, related_name='images_likes', blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = custom_slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
