from rest_framework import serializers
from zinnia.models import Entry

from stocks.models import Securitie


class SecuritiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Securitie
        fields = ('id', 'symbol', 'name', 'exchange', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Securitie
        fields = ('username', 'email', )


class EntrySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Entry
        fields = ('id', 'title', 'text', 'user', )
