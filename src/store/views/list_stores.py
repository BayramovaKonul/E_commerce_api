from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..pagination import StorePagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from ..custom_permissions import IsStoreOwnerOrReadOnly
from drf_yasg import openapi
from ..models import StoreModel
from ..serializers import ListStoreSerializers



class ListStoresView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes=[IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Filter stores by name or description (case-insensitive match).",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Specify the page number for pagination.",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Specify the number of items per page (max 100).",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="A paginated list of stores.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of stores."),
                        "next": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="URL for the next page."),
                        "previous": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="URL for the previous page."),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Store ID"),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING, description="Store name"),
                                    "address": openapi.Schema(type=openapi.TYPE_STRING, description="Store address"),
                                    "website": openapi.Schema(type=openapi.TYPE_STRING, description="Store website"),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING, description="Store description"),
                                    "owner": openapi.Schema(type=openapi.TYPE_STRING, description="Owner name"),
                                },
                            ),
                            description="List of store objects."
                        ),
                    },
                ),
            ),
            400: openapi.Response(description="Bad Request"),
        }
    )
    def get(self, request):
        query_params = dict(request.query_params)
        search=query_params.get('search')  # get search from the request

        stores=StoreModel.objects.all().select_related('owner')
        
        if search:
            stores = stores.filter(Q(name__icontains=search[0]) |
                                       Q(description__icontains=search[0]))
    

        paginator = StorePagination()
        paginated_stores = paginator.paginate_queryset(stores, request)
        serializers=ListStoreSerializers(paginated_stores, many=True)
        return paginator.get_paginated_response(serializers.data)