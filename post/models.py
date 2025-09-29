from django.db import models
from django.utils.text import slugify
from user.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    content = models.TextField()
    image = CloudinaryField('post_image', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from title, fallback to 'post' if title is empty
            base_slug = slugify(self.title) if self.title else 'post'
            if not base_slug:  # If slugify returns empty string
                base_slug = 'post'
            
            self.slug = base_slug
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create slug from user, post title, and timestamp
            import time
            timestamp = self.created_at.strftime('%Y%m%d%H%M%S') if self.created_at else time.strftime('%Y%m%d%H%M%S')
            post_title = slugify(self.post.title) if self.post and self.post.title else 'post'
            username = slugify(self.user.username) if self.user and self.user.username else 'user'
            
            base_slug = f"{username}-{post_title}-{timestamp}"
            self.slug = slugify(base_slug)
            
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Comment.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"