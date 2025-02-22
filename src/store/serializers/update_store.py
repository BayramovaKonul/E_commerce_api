from rest_framework import serializers
from ..models import StoreModel
from .create_store import CreateStoreSerializer
import mimetypes
from django.core.exceptions import ValidationError

class UpdateStoreSerializer(CreateStoreSerializer):
    ...
