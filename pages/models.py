from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError

def validate_nonzero(value):
    if value == 0:
        raise ValidationError("Non-zero values only")
    else:
        return value

class Owner(models.Model):

    """
    A class for the entity that owns a product
    """

    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.id

class Lesson(models.Model):
    code = models.CharField(max_length=255, unique=True)
    length = models.PositiveIntegerField(validators=[validate_nonzero])
    name = models.CharField(max_length=255)
    url = models.URLField()


class User(models.Model):

    """
    A class presenting user who can view lessons and have access to them
    """
    username = models.CharField(
        max_length=255, unique=True
        )
    name = models.CharField(max_length=255)
    date_of_registration = models.TimeField(default=timezone.now)


class Product(models.Model):

    """ A class for storing information about a product """

    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    lesson = models.ManyToManyField(Lesson)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.id


class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, null=True, on_delete=models.SET_NULL)
    lesson_length = models.PositiveIntegerField()
    length_viewed = models.PositiveIntegerField(default=0)
    is_viewed = models.BooleanField(default=False)
    last_viewed = models.DateTimeField(default=timezone.now)
