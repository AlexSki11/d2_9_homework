from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


# Create your models here.
class Author(models.Model):

    author = models.OneToOneField(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating_art = self.post_set.all().aggregate(rating_art=Coalesce(Sum("rating"), 0))['rating_art']
        sum_rating_comment = self.author.comment_set.all().aggregate(rating_comment=Coalesce(Sum("rating"), 0))["rating_comment"]
        sum_rating_comment_post = Comment.objects.filter(comment_post__author_id=self.pk).aggregate(rating_comment_post=Coalesce(Sum("rating"), 0))["rating_comment_post"]



        self.rating = sum_rating_art * 3 + sum_rating_comment + sum_rating_comment_post
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)

class Post(models.Model):
    POST = "PO"
    ARTICLE = "AR"

    CATEGORY_CHOICES = [
        (POST, "Пост"),
        (ARTICLE, "Новость")
    ]

    type_post = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=POST)
    data_create = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through="PostCategory")
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    header = models.CharField(max_length=64)
    text = models.TextField(max_length=20000)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


    def preview(self):
        return f"{self.text[0:123]}..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    rating = models.IntegerField(default=0)
    data_create = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

