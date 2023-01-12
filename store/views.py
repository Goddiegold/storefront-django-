from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serialize import ProductSerializers, CollectionSerializers

# Create your views here.

## route to get all products and a new product##
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializers(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # instead of the above
    # queryset = get_list_or_404(Product)
    # serializer = ProductSerializers(queryset, many=True)
    # return Response(serializer.data)


##route to get a particular product and perform operations like get/put/delete##
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializers(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # instead of the above
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializers(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error': 'Not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###route to get all collection and add a new collection ###
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
        serializer = CollectionSerializers(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


##route to get a particular collection and perform operations like get/put/delete##
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')), pk=pk)

    if request.method == 'GET':
        serializer = CollectionSerializers(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializers(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error':'Something went wrong!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
