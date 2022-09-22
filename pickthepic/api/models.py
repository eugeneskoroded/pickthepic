from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def upload_root(instance, file_name):
    return '{0}/{1}'.format(instance.slug, file_name)


def upload_root_img(instance, file_name):
    return '{0}/{1}'.format(instance.collection.slug, file_name)


class Collection(models.Model):
    name = models.CharField(max_length=200)
    cover = models.ImageField(null=True, blank=True, upload_to=upload_root)
    show = models.BooleanField(default=True)
    slug = models.SlugField(default='', null=False, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('collection-edit', args=[self.slug])


class Image(models.Model):
    image = models.ImageField(upload_to=upload_root_img)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)


class Statistics(models.Model):
    # A scenario
    a_prob = models.FloatField(null=True, blank=True, default=0.5)
    a_views = models.IntegerField(null=True, blank=True, default=0)
    a_views_conv = models.IntegerField(null=True, blank=True, default=0)
    a_conversion = models.FloatField(null=True, blank=True, default=0)
    a_ci_bot = models.FloatField(null=True, blank=True, default=0)
    a_ci_top = models.FloatField(null=True, blank=True, default=0)
    # B scenario
    b_prob = models.FloatField(null=True, blank=True, default=0.5)
    b_views = models.IntegerField(null=True, blank=True, default=0)
    b_views_conv = models.IntegerField(null=True, blank=True, default=0)
    b_conversion = models.FloatField(null=True, blank=True, default=0)
    b_ci_bot = models.FloatField(null=True, blank=True, default=0)
    b_ci_top = models.FloatField(null=True, blank=True, default=0)
