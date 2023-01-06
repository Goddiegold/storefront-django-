from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    labels = models.CharField(max_length=255)



class TaggedItem():
#what tag applied to what item
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

    #to define a generic relationship we need to define tree fields which are content_type, object_id and content_object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()



