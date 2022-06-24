from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class LikedItem(models.Model):
    # What user likes what object
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # content_type: Identify the type of content a user like
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Object ID: for referencing that particular object
    object_id = models.PositiveIntegerField()
    # content_object: For reading an actual object
    content_object = GenericForeignKey()
