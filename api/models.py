from django.db import models
from rest_framework import serializers


class Post(models.Model):

    post_index_main = models.IntegerField(
        blank=True, null=True, verbose_name='Index in news')
    post_index_newest = models.IntegerField(
        blank=True, null=True, verbose_name='Index in newest')
    hn_id = models.IntegerField(
        verbose_name='HN internal id')
    title = models.CharField(
        blank=True, max_length=512, verbose_name='Title')
    url = models.URLField(
        blank=True, verbose_name='Url')
    score = models.CharField(
        blank=True, max_length=512, verbose_name='Score')
    author = models.CharField(
        blank=True, max_length=512, verbose_name='Author')
    comments = models.CharField(
        blank=True, max_length=128, verbose_name='Number of comments')
    posted_ago = models.CharField(
        blank=True, max_length=128, verbose_name='Descriptive text of post age')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('post_index_main',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
