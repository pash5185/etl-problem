from rest_framework import serializers

from etl_app.models import SampleData


class SampleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleData
        fields = ("product_name", "quality", "material_name", "worth", "file_source")
