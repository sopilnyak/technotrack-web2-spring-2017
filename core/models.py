from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.fields import ContentType


class User(AbstractUser):

    objects_count = models.IntegerField(default=0)
    followers = models.ManyToManyField("self")


class ModelWithDate(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelWithAuthor(models.Model):

    author = models.ForeignKey(User)

    class Meta:
        abstract = True


class Event(ModelWithAuthor, ModelWithDate):

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title


class Like(ModelWithAuthor, ModelWithDate):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')


class Likable(models.Model):

    likes = GenericRelation(Like, object_id_field='object_id', content_type_field='content_type')
    likes_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Publication(ModelWithAuthor, ModelWithDate, Likable):

    text = models.CharField(max_length=255)
    edits_count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Comment(Publication):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')


class Commentable(models.Model):

    comments = GenericRelation(Comment, object_id_field='object_id', content_type_field='content_type')
    comments_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Tweet(Publication, Commentable):

    comments_count = models.IntegerField(default=0)
