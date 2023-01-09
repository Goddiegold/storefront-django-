from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection

from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem


# def calculate():
#     x = 1
#     y = 2
#     return x

@transaction.atomic()
def say_hello(request):
    # x = calculate()
    # querysets = Product.objects.all()

    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass

    # instead of the above code
    # product = Product.objects.filter(pk=0).first()

    # for product in querysets:
    #     print(product)

    # querysets = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt = 20))

    # querysets = Product.objects.filter(inventory=F('unit_price'))

    # queryset = Product.objects.order_by('unit_price', '-title').reverse()

    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.order_by('unit_price')[0]

    # products = Product.objects.all()[5:10]

    # products = Product.objects.values('id','title','collection__title')

    # return render(request, 'hello.html', {'name': 'Mosh', 'products': list(products)})

    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    # queryset = Product.objects.defer('description')

    # select related
    # queryset = Product.objects.select_related('collection').all()

    # queryset = Product.objects.prefetch_related('promotions').all()

    # get the last 5 order with their customer and items (incl product)
    # orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # print(orders)

    # result = Product.objects.aggregate(Count('id'), min__price = Min('unit_price'))
    # print(result)

    # results = Customer.objects.annotate(
    #     # is_new=Value(True)
    #     new_id=F('id')
    #     )
    # print(results)

    # queryset  = Customer.objects.annotate(
    #     full_name = Func(F('first_name'), Value(' '),F('last_name'), function='CONCAT')
    # )

    # queryset  = Customer.objects.annotate(
    #     full_name = Concat('first_name', Value(' '), 'last_name')
    # )

    # queryset  = Customer.objects.annotate(
    #     orders_count =Count('order')
    # )

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.9, output_field=DecimalField())
    # queryset  = Product.objects.annotate(
    #     discounted_price = discounted_price
    # )

    # queryset = content_type = ContentType.objects.get_for_model(Product)
    # TaggedItem.objects \
    # .select_related('tag') \
    # .filter(content_type=content_type,
    # object_id=1
    # )
    # print(queryset)

    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product(pk=3)
    # collection.save()

    # collection = Collection.objects.get(pk=11)
    # collection.delete()
    # collection.featured_product = Product(pk=2)
    # collection = Collection.objects.filter(pk=11).update(featured_product=None)
    # collection = Collection.objects.filter(id__gt=5).delete()

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # queryset = Product.objects.raw('SELECT * FROM store_product')
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')

    return render(request, 'hello.html', {'name': 'Mosh', 'products': []})
