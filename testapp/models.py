from django.db import models


class MyModel(models.Model):
    """
    Doesn't include relationships or files for now
    """
    biginteger = models.BigIntegerField()
    boolean = models.BooleanField()
    char = models.CharField(max_length=100)
    csi = models.CommaSeparatedIntegerField(max_length=100)
    date_a = models.DateField()
    datetime_a = models.DateTimeField()
    decimal_a = models.DecimalField(max_digits=5, decimal_places=2)
    email = models.EmailField()
    float_a = models.FloatField()
    integer = models.IntegerField()
    ipaddress = models.IPAddressField()
    genericip = models.GenericIPAddressField()
    nullbool = models.NullBooleanField()
    positiveint = models.PositiveIntegerField()
    positivesmallint = models.PositiveSmallIntegerField()
    slug = models.SlugField()
    smallint = models.SmallIntegerField()
    time_a = models.TimeField()
    url = models.URLField()
