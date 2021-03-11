from django.db import models
from django_countries.fields import CountryField


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True,
                blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_searchable = models.BooleanField(default=True, null=True, blank=True)
    is_presale = models.BooleanField(default=False, null=True, blank=True)
    city = models.ForeignKey('City', null=True,
                blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(blank=True, null=True)
    section = models.ForeignKey('Section', null=True,
                blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name
