from django.db import models


class MyModel(models.Model):
    """
    Doesn't include relationships or files for now
    """
    biginteger = models.BigIntegerField()
    boolean = models.BooleanField()
    char = models.CharField(max_length=100)
    csi = models.CommaSeparatedIntegerField(max_length=100)
    date_ = models.DateField()
    datetime_ = models.DateTimeField()
    decimal_ = models.DecimalField(max_digits=5, decimal_places=2)
    email = models.EmailField()
    float_ = models.FloatField()
    integer = models.IntegerField()
    ipaddress = models.IPAddressField()
    genericip = models.GenericIPAddressField()
    nullbool = models.NullBooleanField()
    positiveint = models.PositiveIntegerField()
    positivesmallint = models.PositiveSmallIntegerField()
    slug = models.SlugField()
    smallint = models.SmallIntegerField()
    time_ = models.TimeField()
    url = models.URLField()
    uuid = models.UUIDField()
