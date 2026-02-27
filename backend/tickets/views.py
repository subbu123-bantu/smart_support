from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket,Category
from .serializers import TicketSerializer,CategorySerializer
from .pagination import CustomPagination
from .filters import TicketFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin,IsAgent,IsCustomer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all() 
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        description = self.request.data.get("description", "").lower()

        if any(word in description for word in ["urgent", "immediately", "critical", "not working", "server down"]):
            priority = "high"
        elif any(word in description for word in ["slow", "delay", "issue"]):
            priority = "medium"
        else:
            priority = "low"

        serializer.save(
            customer=self.request.user,
            priority=priority
        )

    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = TicketFilter
    search_fields = ['title', 'priority', 'description']

    def get_permissions(self):
    
        if self.action == "create":
            return [IsAuthenticated(), IsCustomer()]

        elif self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsAgent()]

        elif self.action == "destroy":
            return [IsAuthenticated(), IsAdmin()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == "CUSTOMER":
            return Ticket.objects.filter(customer=user)

        if user.role == "AGENT":
            return Ticket.objects.filter(assigned_to=user)

        return Ticket.objects.all()

    

    #DefaultFilters
    # {# filter_backend=[DjangoFilterBackend,SearchFilter]
    # filterset_fields=['status']
    # search_fields =['title','periority']
