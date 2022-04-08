from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    return 'news/{filename}'.format(filename=filename)


class News(models.Model):

    class NewsObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1
    )
    title = models.CharField(max_length=250)
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='news/default.jpg')

    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=options, default='published')
    objects = models.Manager()
    newsobjects = NewsObjects()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published',)


class Notification(models.Model):

    class NotificationObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='shown')
    options = (
        ('shown', 'Shown'),
        ('hidden', 'Hidden')
    )

    category = models.ForeignKey(
        Category,  on_delete=models.PROTECT, default=1)
    receipent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notifications')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=options, default='shown')
    objects = models.Manager()
    notifobjects = NotificationObjects()

    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return self.title

class Plate(models.Model):
    def upload_too(instance, filename):
        return 'plates/{filename}'.format(filename=filename)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_plates')
    plate_no = models.CharField(max_length=9,unique=True)
    #image = models.ImageField(_("Image"), upload_to=upload_too,)
    color = models.CharField(max_length=100)
    fuel = models.CharField(max_length=100)
    year = models.IntegerField()
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.plate_no
    
