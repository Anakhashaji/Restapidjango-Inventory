from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer
import logging

logger = logging.getLogger(__name__)

class ItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id=None):
        if item_id:
            # Try to get the item from cache
            cached_item = cache.get(f'item_{item_id}')
            if cached_item:
                logger.info(f"Retrieved item {item_id} from cache")
                return Response(cached_item)

            try:
                item = Item.objects.get(id=item_id)
                serializer = ItemSerializer(item)
                # Cache the item for future requests
                cache.set(f'item_{item_id}', serializer.data, timeout=300)  # Cache for 5 minutes
                logger.info(f"Retrieved item {item_id} from database and cached it")
                return Response(serializer.data)
            except Item.DoesNotExist:
                logger.warning(f"Item {item_id} not found")
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            logger.info("Retrieved all items")
            return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Created new item: {serializer.data['name']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Failed to create item: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            logger.warning(f"Item {item_id} not found for update")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Update the cache
            cache.set(f'item_{item_id}', serializer.data, timeout=300)
            logger.info(f"Updated item {item_id}")
            return Response(serializer.data)
        logger.warning(f"Failed to update item {item_id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            logger.warning(f"Item {item_id} not found for deletion")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        # Remove the item from cache
        cache.delete(f'item_{item_id}')
        logger.info(f"Deleted item {item_id}")
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)