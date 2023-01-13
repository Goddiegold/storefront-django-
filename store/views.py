################################################class based views#########################################
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem, Review
from .serialize import ProductSerializers, CollectionSerializers, ReviewSerializer

# Create your views here.


##Product viewsets##
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0: 
            return Response({'error': 'Not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializers

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({'error': 'Not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def delete(self,request,pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error':'Something went wrong!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}

## route to get all products and a new product##
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers


    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializers

    # def get_serializer_context(self):
    #     return {'request':self.request}

    # def get(self,request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializers(
    #         queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

    # def post(self,request):
    #     serializer = ProductSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     print(serializer.validated_data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)




##route to get a particular product and perform operations like get/put/delete##
# class ProductDetail(RetrieveUpdateDestroyAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializers

    # def get(self,request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializers(product)
    #     return Response(serializer.data)

    # def put(self,request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializers(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

        # def delete(self,request, pk):
        #     product = get_object_or_404(Product, pk=pk)
        #     if product.orderitems.count() > 0:
        #         return Response({'error': 'Not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        #     product.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)



###route to get all collection and add a new collection ###
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializers
    # def get(self,request):
    #     queryset = Collection.objects.annotate(
    #         products_count=Count('products')).all()
    #     serializer = CollectionSerializers(queryset, many=True)
    #     return Response(serializer.data)

    # def post(self,request):
    #     serializer = CollectionSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)



##route to get a particular collection and perform operations like get/put/delete##
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
    # queryset = Collection.objects.annotate(
    #     products_count=Count('products'))
    # serializer_class = CollectionSerializers

    # def get(self,request,pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #     products_count=Count('products')), pk=pk)
    #     serializer = CollectionSerializers(collection)
    #     return Response(serializer.data)

    # def put(self,request,pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #     products_count=Count('products')), pk=pk)
    #     serializer = CollectionSerializers(collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    # def delete(self,request,pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #     products_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error':'Something went wrong!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
        
       
