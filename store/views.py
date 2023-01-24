################################################ class based views#########################################
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order
from .serialize import ProductSerializer,  \
CollectionSerializer, ReviewSerializer, \
 CartSerializer, AddCartItemSerializer,\
  UpdateCartItemSerializer, CartItemSerializer, \
   CustomerSerializer, OrderSerializer, CreateOrderSerializer,\
    UpdateOrderSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission

# Create your views here.


## Product viewsets##

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({'error': 'Not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Something went wrong!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names= ['get','post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
                .filter(cart_id=self.kwargs['cart_pk']) \
                .select_related('product')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self,request,pk):
        return Response('OK')


    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self,request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        


class OrderViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get','patch', 'post', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in [ 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # def get_serializer_context(self):
    #     return {'user_id':self.request.user.id}
    

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

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


## route to get a particular product and perform operations like get/put/delete##
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


### route to get all collection and add a new collection ###
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


## route to get a particular collection and perform operations like get/put/delete##
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
