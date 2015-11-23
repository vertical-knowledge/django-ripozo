from django.db import models


class MyModel(models.Model):
    """
    Doesn't include relationships or files for now
    """
    biginteger = models.BigIntegerField()
    boolean = models.BooleanField(default=False)
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


class OneToMany(models.Model):
    """
    This one model has many ManyToOne models.
    """
    one_value = models.CharField(max_length=63)


class ManyToOne(models.Model):
    """
    Many of this model have one OneToMany models
    """
    one = models.ForeignKey('OneToMany', related_name='manies')
    many_value = models.CharField(max_length=63)


class ManyToManyFirst(models.Model):
    value = models.CharField(max_length=63)


class ManyToManySecond(models.Model):
    value = models.CharField(max_length=63)
    many_to_many = models.ManyToManyField(ManyToManyFirst, related_name='all_the_manies')


class OneFirst(models.Model):
    value = models.CharField(max_length=63)


class OneSecond(models.Model):
    value = models.CharField(max_length=63)
    first = models.OneToOneField(OneFirst, related_name='second')
