from django.db.models.signals import post_save, pre_save, post_init
from .models import ModelWithAuthor, Like, Publication, Comment, Event, Tweet


def publication_init(instance, *args, **kwargs):

    instance.prev_text = instance.text


def publication_presave(instance, created=False, *args, **kwargs):

    if not created and instance.text != instance.prev_text:
        instance.prev_text = instance.text
        instance.edits_count += 1


for model in Publication.__subclasses__():
    post_init.connect(publication_init, model)
    pre_save.connect(publication_presave, model)


def model_with_author_postsave(instance, created=False, *args, **kwargs):

    if created:
        instance.author.objects_count += 1
        instance.author.save()


for model in ModelWithAuthor.__subclasses__():
    post_save.connect(model_with_author_postsave, model)


def like_postsave(instance, created=False, *args, **kwargs):

    if created:
        instance.object.likes_count += 1
        instance.object.save()

        event = Event(author_id=instance.author.pk,
                      type='like',
                      title='User {} liked: "{}" by {}.'
                      .format(instance.author.username, instance.object, instance.object.author.username))
        event.save()


post_save.connect(like_postsave, Like)


def comment_postsave(instance, created=False, *args, **kwargs):

    if created:
        instance.object.comments_count += 1
        instance.object.save()
        event = Event(author_id=instance.author.pk,
                      type='comment',
                      title='User {} commented "{}" by {}: {}.'
                      .format(instance.author.username, instance.object.text,
                              instance.object.author.username, instance.text))
        event.save()


post_save.connect(comment_postsave, Comment)


def tweet_postsave(instance, created=False, *args, **kwargs):

    if created:
        event = Event(author_id=instance.author.pk,
                      type='tweet',
                      title='User {} posted {}.'
                      .format(instance.author.username, instance.text))
        event.save()


post_save.connect(tweet_postsave, Tweet)
