from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible # For Python 3.4 and 2.7
class Aktuelles(models.Model):
    class Meta:
        verbose_name_plural = "Aktuelles"
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    reiselink = models.URLField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
