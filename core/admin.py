from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import User, Tweet, Comment, Like, Event


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    pass


class CommentsInLine(GenericStackedInline):

    model = Comment


class CommentableAdmin(admin.ModelAdmin):

    inlines = CommentsInLine,

    class Meta:
        abstract = True


class LikesInLine(GenericStackedInline):

    model = Like


class LikableAdmin(admin.ModelAdmin):

    inlines = LikesInLine,

    class Meta:
        abstract = True


@admin.register(Tweet)
class TweetAdmin(CommentableAdmin):

    pass


@admin.register(Comment)
class CommentAdmin(LikableAdmin):

    pass


@admin.register(Event)
class CommentAdmin(admin.ModelAdmin):

    pass
