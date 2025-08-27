from rest_framework import generics, permissions
from .models import Alert
from .serializers import AlertSerializer
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# API views
class AlertListCreateView(generics.ListCreateAPIView):
    queryset = Alert.objects.all().order_by('-timestamp')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

class AlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# Template view
@login_required
def alert_list(request):
    alerts = Alert.objects.all().order_by('-timestamp')
    paginator = Paginator(alerts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'alerts/alert_list.html', {'alerts': page_obj})
