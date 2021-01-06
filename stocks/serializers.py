from rest_framework import serializers
from stocks.models import Securities


class SecuritiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Securities
        fields = ('id', 'symbol', 'name', 'exchange', )
