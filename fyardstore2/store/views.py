from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        store_serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(store_serializer.data)

    elif request.method == 'POST':
        # This where deserialization happends
        store_serializer = ProductSerializer(data=request.data)
        store_serializer.is_valid(raise_exception=True)
        store_serializer.save()
        return Response(store_serializer.data, status=status.HTTP_201_CREATED)
    
    # elif request.method == 'POST':
    #     store_data = JSONParser().parse(request)
    #     store_serializer = ProductSerializer(data=store_data)
    #     if store_serializer.is_valid():
    #         store_serializer.save()
    #         return JsonResponse(store_serializer.data,
    #                             status=status.HTTP_201_CREATED)
    #     return JsonResponse(store_serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)  # get product by id
    if request.method == 'GET':
        # create a serializer and give it this product object
        store_serializer = ProductSerializer(product)
        return Response(store_serializer.data)
    elif request.method == 'PUT':
        # This where deserialization happends
        store_serializer = ProductSerializer(product, data=request.data)
        store_serializer.is_valid(raise_exception=True)
        store_serializer.save()
        # Te RESTful convention is to return the product that was created/update
        return Response(store_serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response(
                {'error': 'Product cannot be deleted'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Creating the collection endpoint
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        store_serializer = CollectionSerializer(queryset, many=True)
        return Response(store_serializer.data)
    elif request.method == 'POST':
        store_serializer = CollectionSerializer(data=request.data)
        store_serializer.is_valid(raise_exception=True)
        store_serializer.save()
        return Response(store_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count = Count('products')), pk=pk)

    if request.method == 'GET':
        store_serializer = CollectionSerializer(collection)
        return Response(store_serializer.data)
    elif request.method == 'PUT':
        store_serializer = CollectionSerializer(collection, data=request.data)
        store_serializer.is_valid(raise_exception=True)
        store_serializer.save()
        return Response(store_serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
