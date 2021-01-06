from rest_framework import serializers
from stocks.models import Securitie


class SecuritiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Securitie
        fields = ('id', 'symbol', 'name', 'exchange', )
