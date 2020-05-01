from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy

from account.utils import custom_slugify


class CustomUser(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # user.followers.all() / user.following.all()
    following = models.ManyToManyField('self',
                                       through='Contact',
                                       related_name='followers',
                                       symmetrical=False)
    slug = models.SlugField(max_length=200,
                            blank=True,
                            null=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = custom_slugify(self.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('accounts:user_profile', kwargs={'slug': self.slug})

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,
                                     null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True,
                              null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey(CustomUser,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(CustomUser,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)  # ускорить запросы с фильтрацией и сортировкой по нему

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"
