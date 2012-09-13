from django.db import models
from django.contrib.auth.models import User

# Location
class Location(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    country = models.CharField(max_length=255)
    purpose = models.CharField(max_length=100)
    touch_date = models.DateTimeField(auto_now_add=True, blank=True)
    user_comment = models.TextField()


# For the Person class I am using the built-in User object
# provided by Django's contrib.auth module. From there
# we can extend it out to create a fairly robust Person
# object/user profile type of object.
class Person(models.Model):
    user = models.ForeignKey(User, unique=True)
    location_id = models.ForeignKey(Location)




