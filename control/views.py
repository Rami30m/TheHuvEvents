from django.shortcuts import render
from panel.models import Event, Customers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'control/index.html')
    if request.method == 'POST':
        try:
            decoded = json.loads(request.body)
            uid = decoded.get('data')
            print(uid)
            customer = Customers.objects.get(uid=uid)
            print(customer.name)
            return JsonResponse({'find': True, 'name': customer.name})
        except Customers.DoesNotExist:
            return JsonResponse({'find': False, 'error': 'UID не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'find': False, 'error': str(e)}, status=500)

@login_required
def change_status(request):
    if request.method == 'POST':
        decoded = json.loads(request.body)
        uid = decoded.get('data')

        customer = Customers.objects.get(uid=uid)
        if customer.status == 'attended':
            print("уже есть")
            return JsonResponse({'yet': True})
        customer.status = 'attended'
        customer.save()
        return JsonResponse({'success': True})