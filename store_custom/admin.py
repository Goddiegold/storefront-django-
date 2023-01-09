from django.contrib import admin,contenttypes
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product

# Register your models here.

class TagInline(contenttypes.admin.GenericTabularInline):
    autocomplete_fields=['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)