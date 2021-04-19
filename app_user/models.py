from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils.text import slugify

from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
# Post Model


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='post_images')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=150, blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def draft(self):
        self.published_date = None
        self.save()

    def get_absolute_url(self):
        return reverse("post:my_post")

    def save(self, *args, **kwargs):
        from app_post.views import authorName
        self.author = User.objects.get(username = str(authorName))
        # Try is for delete old image if post update
        try:
            this = Post.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except:
            pass

        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# Function to delete image on delete Post


@receiver(post_delete, sender=Post)
def delete_image_with_post(sender, instance, **kwargs):
    instance.image.delete(False)

# Comment Model


class Comment(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    comment = models.TextField()
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        # sort comments in chronological order by default
        ordering = ('-id',)

    def __str__(self):
        return self.name
