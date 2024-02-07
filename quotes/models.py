from django.db import models
from django.utils.text import slugify
 
# Create your models here.
class ExtendedSlugField(models.SlugField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 500  # Set the desired maximum length
        super().__init__(*args, **kwargs)


class Quote(models.Model):
    USER_TYPE_CHOICES = (
        ('', 'Category'),
        ('Happiness', 'Happiness'),
        ('Hope', 'Hope'),
        ('Life', 'Life'),
        ('Emotion', 'Emotion'),
        ('Empathy','Empathy'),
        ('Pride','Pride'),
        ('Beauty','Beauty'),
        ('Sadness', 'Sadness'),
        ('Anger','Anger'),
        ('Discipline', 'Discipline'),
        ('Fact', 'Fact'),
        ('Guit', 'Guilt'),
        ('Growth', 'Growth'),
        ('Success', 'Success'),
    )
    quote_category = models.CharField(max_length=200, choices=USER_TYPE_CHOICES)
    quote = models.TextField(max_length=500)
    owned_by = models.CharField(max_length=200, blank=True, null=True)
    slug = ExtendedSlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:  # Generate slug only when creating a new object
            self.slug = slugify(self.quote)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.quote_category


