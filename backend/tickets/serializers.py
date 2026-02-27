from rest_framework import serializers
from .models import Ticket,Category

# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model =Ticket
#         fields='__all__'
#         read_only_fields=['customer']

class TicketSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields=['priority']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Category
        fields='__all__'